"""Rewrite a directory of academic papers with Gemini, paragraph-by-paragraph.

Usage:
    python rewrite_papers.py --input-dir papers/human --output-dir papers/ai

Each paragraph is rewritten with the full paper passed as cached context, with
a per-paragraph word-count target. We alternate between gemini-2.5-flash and
gemini-2.5-flash-lite per paper to add model diversity to the AI corpus. Files
that already have an output are skipped, so the script is resumable.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from google import genai
from google.genai import types


PROJECT = "auc-text-mining-antithesis"
LOCATION = "europe-west4"
MODELS = ["gemini-2.5-flash", "gemini-2.5-flash-lite"]

PROMPT = (
    "Rewrite the paragraph below from the academic paper provided as cached "
    "context. Restructure the sentences and reorder the information; don't "
    "just swap synonyms. Don't introduce facts not in the original. Output "
    "plain text, target ~{target_words} words.\n\n"
    "Paragraph:\n{paragraph}\n\n"
    "Rewrite:"
)

# Fallback prompt for papers too short to cache (Vertex minimum ~1024 tokens)
PROMPT_INLINE = (
    "Rewrite the paragraph below from an academic paper. Restructure the sentences "
    "and reorder the information; don't just swap synonyms. Don't introduce facts "
    "not in the original. Output plain text, target ~{target_words} words.\n\n"
    "Full paper for context:\n{full_paper}\n\n"
    "Paragraph:\n{paragraph}\n\n"
    "Rewrite:"
)


def _call(client, model, prompt, cache_name=None):
    config = types.GenerateContentConfig(
        temperature=0.4, max_output_tokens=2048,
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    )
    if cache_name:
        config.cached_content = cache_name
    resp = client.models.generate_content(model=model, contents=prompt, config=config)
    usage = resp.usage_metadata
    stats = {
        "prompt_tokens": getattr(usage, "prompt_token_count", 0) or 0,
        "cached_tokens": getattr(usage, "cached_content_token_count", 0) or 0,
        "output_tokens": getattr(usage, "candidates_token_count", 0) or 0,
    }
    return resp.text or "", stats


def split_paragraphs(text):
    abstract, _, body = text.partition("\n\n")
    paras = []
    for line in body.split("\n"):
        line = line.strip()
        if not line:
            continue
        # Short lines are usually citation fragments like "2,3" or "-17"
        # that PMC XML puts on their own line. Merge into the previous paragraph.
        if paras and len(line.split()) < 15:
            paras[-1] += " " + line
        else:
            paras.append(line)
    return [abstract] + paras


def _make_cache(client, model, full_paper):
    """Create a cached context for the full paper. Returns cache name or None."""
    try:
        cache = client.caches.create(
            model=model,
            config=types.CreateCachedContentConfig(
                contents=[types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=f"Full paper for context:\n{full_paper}")],
                )],
                ttl="1800s",
            ),
        )
        return cache.name
    except Exception as exc:
        # Most common reason: paper too short for the cache minimum
        print(f"(cache skipped: {type(exc).__name__})", end=" ", flush=True)
        return None


def rewrite_paper(client, model, text):
    paras = split_paragraphs(text)
    cache_name = _make_cache(client, model, text)

    out = []
    totals = {"prompt_tokens": 0, "cached_tokens": 0, "output_tokens": 0}
    try:
        for p in paras:
            target = len(p.split())
            if cache_name:
                prompt = PROMPT.format(target_words=target, paragraph=p)
                rewrite, stats = _call(client, model, prompt, cache_name=cache_name)
            else:
                prompt = PROMPT_INLINE.format(target_words=target, full_paper=text, paragraph=p)
                rewrite, stats = _call(client, model, prompt)
            out.append(" ".join(rewrite.split()))
            for k in totals:
                totals[k] += stats[k]
    finally:
        if cache_name:
            try:
                client.caches.delete(name=cache_name)
            except Exception:
                pass

    return out[0] + "\n\n" + "\n".join(out[1:]), totals


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process at most this many input files (useful for testing).",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    inputs = sorted(args.input_dir.glob("*.txt"))
    if args.limit:
        inputs = inputs[: args.limit]
    if not inputs:
        print(f"No .txt files in {args.input_dir}", file=sys.stderr)
        return 1

    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)

    processed: list[str] = []
    per_paper_usage: dict = {}
    for i, path in enumerate(inputs):
        out_path = args.output_dir / path.name
        if out_path.exists():
            print(f"skip {path.name}: already done")
            continue

        model = MODELS[i % len(MODELS)]
        text = path.read_text()
        print(f"rewriting {path.name} ({len(text)} chars) with {model}...", end=" ", flush=True)
        start = time.time()
        try:
            rewrite, totals = rewrite_paper(client, model, text)
        except Exception as exc:
            print(f"FAILED: {exc}")
            continue
        out_path.write_text(rewrite)
        processed.append(path.name)
        per_paper_usage[path.name] = {"model": model, **totals}
        cached_pct = (totals["cached_tokens"] / totals["prompt_tokens"] * 100) if totals["prompt_tokens"] else 0
        print(f"done in {time.time() - start:.1f}s, "
              f"in={totals['prompt_tokens']:,} (cached={cached_pct:.0f}%), "
              f"out={totals['output_tokens']:,}")

    if processed:
        runs_dir = args.output_dir.parent / "runs"
        runs_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        manifest = {
            "timestamp_utc": stamp,
            "models": MODELS,
            "project": PROJECT,
            "location": LOCATION,
            "temperature": 0.4,
            "max_output_tokens": 2048,
            "thinking_budget": 0,
            "prompt": PROMPT,
            "input_dir": str(args.input_dir),
            "output_dir": str(args.output_dir),
            "papers": processed,
            "usage": per_paper_usage,
        }
        (runs_dir / f"{stamp}.json").write_text(json.dumps(manifest, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
