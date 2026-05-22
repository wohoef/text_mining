# Project Readme

## Title
Uncovering Characteristics of Artificial Intelligence Writing Using Stylometric and Linguistic Features

## Abstract
The introduction of Large Language Models (LLMs) has raised questions about their influence on human language. This influence can occur directly, through users copying LLM output, or indirectly, through humans adopting the linguistic patterns of LLMs. Because of this, identifying stylometric and linguistic features that distinguish AI-generated text from human writing has become an area of growing interest. This study focuses on extracting textual features from a set of human-written articles downloaded from PubMed and a set of AI-generated rewrites, and using these features to train a logistic regression classifier. This model was chosen to prioritize interpretability, allowing us to use the resulting coefficients to determine which features are most indicative of a paper being AI-generated or human-written.

## Research question
Which extracted stylometric and linguistic features of scientific text are most indicative of it being AI-generated rather than human-written?

## Dataset
Our dataset consists of two subsets of 200 articles each: a human-generated subset and an AI-generated subset. The human-generated subset was derived from PubMed, retrieving scientific papers published between 2000 and 2019. The AI-generated subset was created by feeding the original human subset to the Gemini API and having it rewrite each paper in its own words, producing a subset that is fully AI-generated. Together these subsets form a balanced, paired corpus used to train and evaluate the classifier.

### Human-Generated Dataset
This subset was obtained by downloading articles published between 2000 and 2019. Since LLMs were not yet in use during this period, this date range ensures that all articles were written solely by humans. The articles were downloaded using the PubMed API, which returns article identifiers within a given date range. With these identifiers, the article content was retrieved in XML format, and the body text was filtered and extracted into .txt files.

### AI-Generated Dataset
As no suitable AI-generated scientific text was available online, we created this subset ourselves. Using the Gemini API, each human paper was rewritten paragraph-by-paragraph, with each original paragraph's length used as a word-count target so the AI version stays roughly the same length as the original. The rewrite prompt is shown below:

> "Rewrite the paragraph below from the academic paper provided as cached context. Restructure the sentences and reorder the information; don't just swap synonyms. Don't introduce facts not in the original. Output plain text, target ~{target_words} words. Paragraph: {paragraph} Rewrite:"

The output obtained from the API forms the AI-generated subset.

## Features
Our logistic regression model looks at a variety of features. Some of these features were selected from existing literature, and others were added along the way. The features that the model takes as input are the following:
- Average sentence length
- Average word length
- Type-to-token ratio
- The variation of sentence lengths (burstiness)
- Average parse tree depth
- Percentage of words that are associated with AI writing according to the literature
- Percentage of words that we found to be used more in our AI (train) dataset
- Function word rates (pronouns, adpositions, determiners, conjunctions, and auxiliary verbs)

## A Tentative List of Milestones
Project Update 0 - April 14
- Repository and README [Everyone]

Project Update 1 - April 28
- Update README to new plan [Melle]
- Write model fitting code [Wout]
- Create pipeline to AI-ify papers [Jonathan]

Project Update 2 - May 8
- Have a script to download pubmed articles and extract the text [Leticia]
- Collect dataset using script [Leticia]
- Add a few more features to our training data [Leticia]
- Update README [Melle]
- Create textual features Python script [Wout]

In-class Presentations - May 19/22
- Presentation prepared [Everyone]
- First draft of the report done [Everyone]
- Abstract [Leticia]
- Introduction [Jonathan]
- Related work [Leticia]
- Data collection [Wout]
- Methodology [Wout]
- Results and findings [Leticia]
- Discussion [Melle]
- Limitations [Melle]
- Future work [Jonathan]
- Conclusions [Wout]

Final Deadline - May 22
- Clean up the repository and the report [Everyone]

## Documentation
- **[main.ipynb](https://github.com/wohoef/text_mining/blob/main/main.ipynb)**: Main notebook where the logistic regression model is trained on the corresponding text features. The data is first uploaded and tokenized. Then the model is trained and the corresponding confusion matrix, feature coefficients and AI-word use metrics are extracted.

- **[model_comparison.ipynb](https://github.com/wohoef/text_mining/blob/main/model_comparison.ipynb)**: This is an additional notebook where we tested multiple models (XGBoost and HistGradientBoosting) prior to choosing logistic regression. We ended up opting for the one which we thought was more interpretable as we wanted to focus on this throughout the report.

- **[requirements.txt](https://github.com/wohoef/text_mining/blob/main/requirements.txt)**: Python dependencies required to run the code.

- **[docs/methodology_notes.md](https://github.com/wohoef/text_mining/blob/main/docs/methodology_notes.md)**: Notes on corpus construction, alternatives considered, and limitations of the chosen setup.

- **[docs/gemini_api_guide.md](https://github.com/wohoef/text_mining/blob/main/docs/gemini_api_guide.md)**: Setup guide for calling Gemini through the shared Google Cloud project.

- **[scripts/check_split.py](https://github.com/wohoef/text_mining/blob/main/scripts/check_split.py)**: Utility to verify the paragraph splitter's output before bulk rewriting runs.

- **[scripts/fetch_articles.py](https://github.com/wohoef/text_mining/blob/main/scripts/fetch_articles.py)**: Python script to automatically download PubMed articles as .txt using the API.

- **[scripts/model_functions.py](https://github.com/wohoef/text_mining/blob/main/scripts/model_functions.py)**: Functions that are used in both main.ipynb and model_comparison.ipynb to avoid repetitive code.

- **[scripts/rewrite_papers.py](https://github.com/wohoef/text_mining/blob/main/scripts/rewrite_papers.py)**: Python script that uses the Gemini API to rewrite each human paper paragraph-by-paragraph, producing the AI dataset.

- **[scripts/text_features.py](https://github.com/wohoef/text_mining/blob/main/scripts/text_features.py)**: Python script containing the text features extracted from every article.


**Removed due to licensing**
- **ai_articles**: Folder containing the AI-generated papers, one .txt file per paper. Output of rewrite_papers.py.
- **human_articles**: Folder containing the human-written PubMed papers, one .txt file per paper. Output of fetch_articles.py.
