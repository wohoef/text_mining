"""Rewrite a directory of academic papers with Gemini, paragraph-by-paragraph.

Usage:
    python rewrite_papers.py --input-dir papers/human --output-dir papers/ai

Each paragraph is rewritten with the full paper passed as context, with a
per-paragraph word-count target and a one-shot retry if the rewrite is too
short. Files that already have an output are skipped, so the script is
resumable.
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
DEFAULT_MODEL = "gemini-2.5-flash"

PROMPT = (
    "Rewrite the paragraph below from an academic paper. Restructure the sentences "
    "and reorder the information; don't just swap synonyms. Don't introduce facts "
    "not in the original. Output plain text, target ~{target_words} words.\n\n"
    "Full paper for context:\n{full_paper}\n\n"
    "Paragraph:\n{paragraph}\n\n"
    "Rewrite:"
)


def _call(client, model, prompt):
    resp = client.models.generate_content(
        model=model, contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.4, max_output_tokens=2048,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )
    return resp.text or ""


def split_paragraphs(text):
    abstract, _, body = text.partition("\n\n")
    return [abstract] + [p for p in body.split("\n") if p.strip()]


def rewrite_paragraph(client, model, full_paper, paragraph):
    target = len(paragraph.split())
    prompt = PROMPT.format(target_words=target, full_paper=full_paper, paragraph=paragraph)
    text = _call(client, model, prompt)
    if len(text.split()) < 0.85 * target:
        text = _call(client, model, prompt + f"\n\nToo short, aim for ~{target} words.")
    return " ".join(text.split())


def rewrite_paper(client, model, text):
    paras = split_paragraphs(text)
    out = [rewrite_paragraph(client, model, text, p) for p in paras]
    return out[0] + "\n\n" + "\n".join(out[1:])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
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
    for path in inputs:
        out_path = args.output_dir / path.name
        if out_path.exists():
            print(f"skip {path.name}: already done")
            continue

        text = path.read_text()
        print(f"rewriting {path.name} ({len(text)} chars)...", end=" ", flush=True)
        start = time.time()
        try:
            rewrite = rewrite_paper(client, args.model, text)
        except Exception as exc:
            print(f"FAILED: {exc}")
            continue
        out_path.write_text(rewrite)
        processed.append(path.name)
        print(f"done in {time.time() - start:.1f}s, wrote {len(rewrite)} chars")

    if processed:
        runs_dir = args.output_dir.parent / "runs"
        runs_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        manifest = {
            "timestamp_utc": stamp,
            "model": args.model,
            "project": PROJECT,
            "location": LOCATION,
            "temperature": 0.4,
            "max_output_tokens": 2048,
            "thinking_budget": 0,
            "prompt": PROMPT,
            "input_dir": str(args.input_dir),
            "output_dir": str(args.output_dir),
            "papers": processed,
        }
        (runs_dir / f"{stamp}.json").write_text(json.dumps(manifest, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
