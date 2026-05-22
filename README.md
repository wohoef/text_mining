# Project Readme

## Title
General Text Characteristics in Artificial Intelligence (AI) Scientific Writing

## Abstract
Large language models (LLMs) are increasingly used in scientific writing, raising the question of whether AI-generated text can be reliably distinguished from human-written text. This project builds a paired corpus of human papers and their AI rewrites, and trains a classifier to tell them apart using a set of interpretable text features. Rather than relying only on known "AI vocabulary" such as "delve" or "align", we also measure structural and stylistic characteristics: sentence and word length, lexical diversity, burstiness, parse tree depth, and function-word usage. We train a logistic regression model on these features and use its coefficients to determine which characteristics are most indicative of AI-generated scientific writing.

Our dataset consists of two subsets: a human-generated subset and an AI-generated subset. The human subset was downloaded from PubMed (papers published 2000-2019, before LLMs were in use). The AI subset was created by passing each human paper to the Gemini API and having it rewrite the paper paragraph-by-paragraph, producing a corpus that is fully AI-generated.

## Research questions
- What characteristics of text are most indicative of it being AI-generated in scientific papers?
- (discussion) To what extent can the prevalence of “AI characteristic” vocabulary and sentence structures be used to detect AI use?

## Dataset
As mentioned in the abstract, our dataset consists of two subsets.

### Human-Generated Dataset
This subset was obtained by downloading articles published between 2000 and 2019. Since LLMs were not yet in use during this period, this date range ensures the articles were written solely by humans. The articles were downloaded via the PubMed API, which returns article identifiers within a given date range; the article content was then retrieved in XML format and the body text filtered and extracted into .txt files.

### AI-Generated Dataset
As no suitable AI-generated scientific text was available online, we created this subset ourselves. Using the Gemini API, each human paper was rewritten paragraph-by-paragraph, with each original paragraph's length used as a word-count target so the AI version stays roughly the same length as the original. The full rewrite prompt is defined in `scripts/rewrite_papers.py`. This produced the AI-generated subset.

## Features
The model uses the following text features, extracted over 5-sentence sliding windows:
- Average sentence length
- Average word length
- Type-to-token ratio
- Burstiness (variation in sentence length)
- Average parse tree depth
- Function-word rates (pronouns, adpositions, determiners, conjunctions, auxiliary verbs)
- Rate of AI-associated vocabulary from the literature (e.g. "delve", "align", "intricate")
- Rate of vocabulary found to occur more often in the AI training set

## A Tentative List of Milestones
Project Update 0 - April 14
- Repository and README [Everyone]

Project Update 1 - April 28
- Update README to new plan [Melle]
- Write model fitting code [Wout]
- Create pipeline to AI-ify papers [Jonathan]

Project Update 2 - May 8
- Have a script to download pubmed articles and extract the text
- Collect dataset using script
- Add a few more features to our training data
- Analyze results and create base for the report

In-class Presentations - May 19/22
- Presentation prepared [Everyone]
- First draft of the report done
- Abstract [Jonathan]
- Introduction [Leticia] 
- Related work [Melle]
- Data collection [Wout]
- Dataset description with summary statistics [Melle]
- Methods with math and description of main algorithms [Leticia]
- Results and findings [Jonathan]
- Conclusions [Jonathan]

Final Deadline - May 22
- Implement feedback to report and code
- Clean up the repository and the report

## Getting Started
The project entry point is **`main.ipynb`**. It loads the human and AI corpora, extracts text features, trains the logistic regression model, and displays the results. To reproduce the corpus from scratch first run `scripts/fetch_articles.py` (downloads the human papers) and `scripts/rewrite_papers.py` (generates the AI rewrites); otherwise the `human_articles/` and `ai_articles/` folders already contain the dataset used in the report.

Install dependencies with `pip install -r requirements.txt`.

## Repository Structure
- **`main.ipynb`**: Main notebook — data prep, feature extraction, logistic regression training, and results (confusion matrix and feature analysis).
- **`model_comparison.ipynb`**: Compares logistic regression against XGBoost and HistGradientBoosting.
- **`scripts/fetch_articles.py`**: Downloads PubMed articles (2000-2019) as .txt files via the API.
- **`scripts/rewrite_papers.py`**: Rewrites each human paper paragraph-by-paragraph with the Gemini API to produce the AI dataset.
- **`scripts/check_split.py`**: Verifies the paragraph splitter's output before bulk rewriting runs.
- **`scripts/text_features.py`**: Extracts the text features used by the model.
- **`scripts/model_functions.py`**: Corpus loading, AI-vocabulary learning, and dataset/group construction.
- **`docs/gemini_api_guide.md`**: Setup guide for calling Gemini through the shared Google Cloud project.
- **`docs/methodology_notes.md`**: Notes on corpus construction, alternatives considered, and limitations of the chosen setup.
- **`requirements.txt`**: Python dependencies required to run the code.
- **`human_articles/`**: Human-written PubMed papers, one .txt file per paper. Output of `fetch_articles.py`.
- **`ai_articles/`**: AI-rewritten papers, one .txt file per paper. Output of `rewrite_papers.py`.
- **`runs/`**: Run manifests logging the settings and token usage for each rewrite run.

