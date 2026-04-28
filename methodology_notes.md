# Methodology notes

## Corpus construction

The corpus is built from roughly 100 academic papers published before 2021 (predating ChatGPT's public release). Each paper provides two parallel inputs to the classifier:

- **Human side:** the original published text.
- **AI side:** an LLM rewrite of the same content, produced by feeding the human text to a generative model and asking it to rephrase the passage in its own words.

Because both sides start from the same source content, the human-vs-AI signal the classifier learns should reflect stylistic and structural choices specific to the AI rather than topic, terminology, or domain conventions.

## Alternatives considered

### Time-split as a proxy for AI authorship

Compare academic prose from a pre-ChatGPT cohort (e.g. 2021) against a post-ChatGPT cohort (e.g. 2025) and treat the year as a label. Rejected because there is no way to verify which post-ChatGPT papers were actually written or edited with LLM assistance. Any classifier built this way would attribute every difference between cohorts (topic drift, evolving citation conventions, changes in journal style, the growing share of papers from new fields) to AI exposure, when in fact most of the variance has nothing to do with it.

### Public AI-vs-human datasets

Publicly available labeled corpora such as Hello-SimpleAI/HC3 or `ai-text-detection-pile` exist. These are typically built from question-answer pairs or short essays, not academic prose, so a classifier trained on them would be evaluated on a different domain from the one we want to make claims about. They remain useful as an external sanity check, but the headline evaluation should sit on our own corpus.

### Fully AI-generated papers (no human seed)

Asking an LLM to write academic papers from scratch produces uniformly synthetic output that does not resemble how published work is actually produced (which involves iteration, editing, and at most partial AI assistance). The signal would be artificially strong and would not generalize to the realistic mixed-authorship setting that is the actual research target.

## Limitations of the chosen approach

- **Conditioning effect.** The AI rewrite is generated from the human paper, so the AI side carries some content and structural information from the human source. The human-vs-AI difference detected by the classifier is therefore a lower bound on what fully independent AI text would look like.
- **Model and prompt sensitivity.** Small changes in model or prompt wording can substantially alter generation behavior. Findings should either span enough variation across these choices to be considered robust, or be scoped explicitly to the specific model and prompt used.
- **Cleanliness of the AI side.** Real published papers post-ChatGPT are typically partly AI-assisted rather than pure AI rewrites, so our AI side is artificially "clean." Generalizing from this setup to real-world detection of mixed-authorship text requires additional validation.

## Scope of claims

Given the limitations above, results from this corpus should be framed as detectable stylistic differences between human academic prose and one specific AI-rewriting setup. Stronger claims about authorship in real published literature, or about AI text in general, would require additional evidence beyond this corpus.
