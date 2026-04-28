# Dataset options for AI-vs-human classification

Three paths, in order of recommendation.

## Option A (recommended): Use a public Hugging Face dataset

Direct labeled AI-vs-human pairs, no proxy needed. Huge time saver versus building our own.

| Dataset | Size | Notes |
|---|---|---|
| `Hello-SimpleAI/HC3` | ~24k pairs | Gold standard. Human ChatGPT Comparison Corpus, English + Chinese, multi-domain (open, finance, medical, legal, psychology). Paper: arXiv:2301.07597. https://hf.co/datasets/Hello-SimpleAI/HC3 |
| `artem9k/ai-text-detection-pile` | 1M-10M | Long-form essays. Ideal if we want to test on essay-style text. https://hf.co/datasets/artem9k/ai-text-detection-pile |
| `silentone0725/ai-human-text-detection-v1` | 10k-100k | Merges 9 public corpora. Useful for diversity. https://hf.co/datasets/silentone0725/ai-human-text-detection-v1 |

**What to do:**
```python
from datasets import load_dataset
ds = load_dataset("Hello-SimpleAI/HC3", "all")
# columns: question, human_answers, chatgpt_answers, source
```

This single dataset gives us a clean train/test split, a reference paper to cite, and removes the time-split proxy entirely. We can still keep the academic-papers angle as a "transfer evaluation" set.

## Option B: Time-split proxy (Jonathan's idea)

Treat year of publication as a stand-in for AI exposure.

- **Pre-ChatGPT cohort**: academic papers published in **2021** (ChatGPT's public release was Nov 2022, so 2021 is unambiguously human).
- **Post-ChatGPT cohort**: academic papers published in **2025** (everyone has access; high prior of LLM influence).
- Pull a balanced sample, e.g. 50 + 50, normalized for field.

**Limitations to call out in the report:**
- Confounded with topic drift, citation conventions evolving, etc.
- Doesn't isolate AI authorship; measures "post-ChatGPT trend." That's a real research question, just not the same as "AI vs human."

## Option C: Hybrid (best of both)

1. Train on HC3 (clean labels, fast iteration).
2. Hold out an academic-paper test set built from Option B's 2021 vs 2025 split.
3. Evaluate transfer: does a classifier trained on Q&A pairs generalize to academic prose? This is itself a publishable angle.

## What we already have (in the Doc)

The Gender Studies papers everyone has been adding (Leticia 9, Jonathan 5, Melle 0+) can serve as a transfer test set under any of the three options. Year of each paper determines its bucket in B or C.

## Recommended call

**Go with A** for the MVP today. Option A with HC3 = working pipeline by tonight. The reason Leticia couldn't find a labeled AI-vs-human dataset is probably search wording: HC3 and the detection pile are well-known but tagged as "ChatGPT detection" rather than "AI vs human." They're there.

Add Option C as a secondary evaluation in the report once the MVP works.
