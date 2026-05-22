# Project Readme

## Title
General Text Characteristics in Artificial Intelligence (AI) Scientific Writing

## Abstract
The introduction of Large Language Models (LLMs) has raised questions about their influence in human language. This influence can occur directly through users copying the output of an LLM, or indirectly through humans mirroring the language usage by LLMs. Current research focuses on analyzing the frequency of certain words like “delve” and “align”, given that LLMs use these disproportionately often. Going beyond this, in this research we will investigate whether, similarly to the increase of specific vocabulary, certain other characteristics have also increased. Some characteristics we will explore include:
- Average sentence/word length
- Number of nouns/verbs
- Perplexity
- Type/token ratio

We will train a logistic regression model on these features. Using the coefficients obtained from this model, we will then determine the importance of each characteristic in correctly classifying a paper as AI or not.

Our datasets consist of two subsets: a human-generated subset and an AI-generated subset. The human-generated subset will be derived from PubMed, where we will retrieve scientific papers published between 2000-2019. The AI-generated subset will be created by feeding the original human subset to the API of the Gemini LLM, and asking it to rewrite these papers in its own words, creating a dataset we are sure is fully AI-made. Using these two datasets, we will analyze the evolution of these characteristics, highlighting any correlations observed with AI use.

## Research questions
- What characteristics of text are most indicative of it being AI-generated in scientific papers?
- (discussion) To what extent can the prevalence of “AI characteristic” vocabulary and sentence structures be used to detect AI use?

## Dataset
As mentioned in the abstract, our dataset consists of two subsets.

### Human-Generated Dataset
This dataset will be obtained from downloading a large number of articles between 2000 - 2019. Since LLMs were not yet used during this period, this date range ensures that all articles are written solely by humans. These articles will be downloaded using the PubMed API which allows us to obtain any number of article identifiers during our defined time range. With these identifiers, the content of the articles can be extracted in XML format from which text can be filtered and extracted to output .txt files.

### AI-Generated Dataset
As no promising AI-generated scientific article text was found online, we decided to manually create this dataset ourselves. For the purposes of time efficiency, we set up a Geminini API, which will take the human-generated dataset and a prompt such as "Rewrite these articles in your own words", and output a new dataset which we call the AI-generated dataset. 

## Features
The model will look at a variety of features. Ideally we pick as many as possible to see which features carry most signal. Some features we can consider adding include:
- Average sentence/word length
- Number of nouns/verbs
- Perplexity
- Type/token ratio
- Burstiness
- Average parse tree depth
- Hapax legomena ratio
- Flesch-Kincaid / readability scores
- Frequency of AI-words like "delve", "align" and "intricate"

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

