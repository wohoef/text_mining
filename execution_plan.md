# Execution plan: AI-vs-human text classifier

After the antithesis pivot fell through (Leticia's manual annotation found basically no examples in academic papers), the project shifted to a binary classifier of AI vs human text using interpretable, hand-crafted features. This document is the dependency-ordered plan for that direction.

## Phase 0 : Decisions

- [x] **D1. Task type.** Binary classification: AI vs human text. Document-level (one prediction per text).
- [x] **D2. Model.** Logistic regression as the headline model (chosen for interpretability: per-feature coefficients become the "what makes text look AI" answer). Optionally add a Random Forest as a second baseline.
- [ ] **D3. Dataset.** See `dataset_options.md`. Recommended: Hugging Face `Hello-SimpleAI/HC3` for training, with the 2021 vs 2025 academic-paper split as a transfer test set.
- [x] **D4. Feature set.** See `feature_candidates.md`. Start with the ~10-feature MVP bundle; add syntactic features later if F1 is weak.

## Phase 1 : Data

Prereq: D3.

- [ ] **1a. Pull HC3** via `datasets.load_dataset("Hello-SimpleAI/HC3", "all")`. Save to `data/raw/`.
- [ ] **1b. Clean and balance.** Strip empty answers, normalize whitespace, balance classes. Save to `data/processed/`.
- [ ] **1c. Train/val/test split.** 70 / 15 / 15, stratified by class.
- [ ] **1d. (Optional) Build the academic-paper transfer set** from the existing Gender Studies papers + supplemental 2021 and 2025 papers. Saves a parallel evaluation file.

## Phase 2 : Feature engineering

Prereq: 1b.

- [ ] **2a. Tokenize and POS-tag** with spaCy (`en_core_web_sm`). Cache to disk so we don't re-run.
- [ ] **2b. Compute MVP features** (10 in `feature_candidates.md`): length stats, MATTR, function-word freqs, POS rates, em-dash rate, comma rate, AI-tell score, trigram repetition.
- [ ] **2c. Stack into a feature matrix** (numpy / pandas). One row per document.
- [ ] **2d. (Optional) Add syntactic features** (parse-tree depth, dep distance, clause count) if MVP F1 is below ~0.75.

## Phase 3 : Modeling

Prereq: 1c, 2c.

- [ ] **3a. Fit logistic regression** on training set. L2 regularization, default C.
- [ ] **3b. Evaluate** on val: precision, recall, F1, accuracy, confusion matrix.
- [ ] **3c. Coefficient inspection.** Sort features by absolute coefficient. This is the "what's predictive" table for the report.
- [ ] **3d. Optional: Random Forest baseline** for comparison.
- [ ] **3e. Test-set evaluation.** Lock the test set, run once, report.

## Phase 4 : Transfer evaluation (optional but high-value)

Prereq: 3a, 1d.

- [ ] **4a. Apply trained model** to academic-paper transfer set (2021 vs 2025).
- [ ] **4b. Report rate** of "AI-like" predictions in each cohort. This addresses RQ1 directly: has academic prose drifted toward AI characteristics post-ChatGPT?
- [ ] **4c. Statistical test** for the difference (chi-square or Mann-Whitney on prediction scores).

## Phase 5 : Report and presentation

Prereq: 3e.

- [ ] **5a. Slide deck.** 5-10 slides: motivation, RQs, dataset, features, model, results, transfer findings.
- [ ] **5b. 4-page report.** Abstract, intro, related work, data, methods, results, conclusions, contributions.
- [ ] **5c. Repo cleanup.** README with reproduction instructions, single main notebook, remove dead code.

## What about Vertex / Gemini?

The Vertex AI setup (see `AI_ACCESS.md`) is no longer on the critical path because we have HC3 as labeled training data, removing the LLM weak-labeling step. Keep the access alive for two contingency uses:
1. Generate additional AI-side text on academic topics if the transfer set needs more data.
2. Quick prompt-based labeling if we want to add a non-HC3 domain.

## Critical-path summary

```
D1,D2,D3,D4 → 1a → 1b → 1c → 2a → 2b → 2c → 3a → 3b → 3c → 3e → 5a,5b,5c
            ↘ 1d ────────────────────────────→ 4a → 4b → 4c ↗
```

The whole thing is much shorter than the BERT plan. MVP is realistically a single afternoon once the dataset is downloaded.

## Task assignments (from WhatsApp, 28 April)

- **Wout:** main code (read datasets, np matrices, fit scikit-learn). Covers Phases 1, 2, 3.
- **Leticia:** find feature/metric sources from literature. Overlaps `feature_candidates.md`.
- **Jonathan:** AI access PDF + dataset curation. This PR. Then Phase 4 transfer set + report sections.
- **Melle:** README rewrite (still TBD).

## What's in this PR

- `AI_ACCESS.md` and `AI_ACCESS.pdf`: Gemini access setup, per Leticia's request.
- `feature_candidates.md`: starter feature list with literature pointers.
- `dataset_options.md`: HC3 and alternatives, replacing the time-split-only proxy.
- `execution_plan.md`: this file. The new direction.
- `README.md`: updated documentation section to link the new files.

Not merging this PR automatically. The group should review the new direction before it lands on `main`.
