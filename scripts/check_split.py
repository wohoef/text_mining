"""Dry-run the splitter on a directory of papers and print per-paper stats.

Use this to sanity-check that no paper produces hundreds of micro-paragraphs
or other anomalies before spending API budget on a bulk run.

Usage:
    python check_split.py --input-dir all_articles
"""

import argparse
from pathlib import Path

from scripts.rewrite_papers import split_paragraphs  # own library


# ------------------------------------------------
def main():
    """
    Splits every .txt paper in the input directory and prints a table of
    per-paper paragraph stats, then flags papers that look suspicious.
    """
    # Read the input directory from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for path in sorted(args.input_dir.glob("*.txt")):
        # Load the raw text
        text = path.read_text()

        # Split the text into paragraphs
        paras = split_paragraphs(text)

        # Count the words in each paragraph
        word_counts = [len(p.split()) for p in paras]

        # Store one row of stats per paper
        rows.append((path.name, len(paras), min(word_counts), max(word_counts), sum(word_counts)))

    # Print the stats table
    print(f"{'paper':<20} {'paras':>6} {'min_words':>10} {'max_words':>10} {'total':>8}")
    for name, n, mn, mx, total in rows:
        print(f"{name:<20} {n:>6} {mn:>10} {mx:>10} {total:>8}")

    # Flag papers that may have been split badly
    print()
    print(f"papers with >50 paragraphs (suspicious): "
          f"{sum(1 for r in rows if r[1] > 50)}")
    print(f"papers with any para <5 words (suspicious): "
          f"{sum(1 for r in rows if r[2] < 5)}")


if __name__ == "__main__":
    main()
