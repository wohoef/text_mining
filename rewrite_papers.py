"""Rewrite a directory of academic papers with Gemini, paper-by-paper.

Usage:
    python rewrite_papers.py --input-dir papers/human --output-dir papers/ai

Each `*.txt` in `--input-dir` is sent to the model in one call, and the
rewrite is written to a same-named file under `--output-dir`. Files that
already have an output are skipped, so the script is resumable.
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
    "Rewrite the academic paper below in your own words, paragraph by "
    "paragraph. Constraints:\n"
    "- Preserve every claim, argument, section, and the order in which "
    "they appear.\n"
    "- Preserve equations, mathematical notation, citations, and reference "
    "list entries verbatim.\n"
    "- Do not summarize, omit, expand, or reorder content.\n"
    "- Match the register and length of the original.\n"
    "- Output plain text only, no markdown.\n\n"
    "Original:\n\n{text}\n\nRewrite:"
)


def rewrite_one(client: genai.Client, model: str, text: str) -> str:
    response = client.models.generate_content(
        model=model,
        contents=PROMPT.format(text=text),
        config=types.GenerateContentConfig(
            temperature=0.0,
            max_output_tokens=65536,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )
    return response.text or ""


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
            rewrite = rewrite_one(client, args.model, text)
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
            "temperature": 0.0,
            "max_output_tokens": 65536,
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
