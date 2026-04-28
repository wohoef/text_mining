# Project Readme

## Title
General Text Characteristics in Human and AI Writing

## Abstract
The introduction of Large Language Models (LLMs) has raised questions about their influence in human language. This influence can occur directly through users copying the output of an LLM, or indirectly through humans mirroring the language usage by LLMs. Current research focuses on analyzing the frequency of certain words like “delve” and “align”, given that LLMs use these disproportionately often. Going beyond this, in this research we will investigate whether, similarly to the increase of specific vocabulary, certain other characteristics have also increased. Some characteristics we will explore include:
- Average sentence/word length
- Number of nouns/verbs
- Perplexity
- Type/token ratio
We will train a logistic regression model on these features. Then we use the coefficients of this model to determine the importance of each characteristic.
With gender studies papers published between 2015-2020, we'll use LLM's to rewrite these papers and creata a generated counterpart. Between these two dataset we'll then analyse the evolution of these characterisitcs, highlighting correlations with AI use. We'll use a webscraper to collect the papers.

## Research questions
- What characteristics of text are most indicative of it being AI-generated?
- (discussion) To what extent can the prevalence of “AI characteristic” vocabulary and sentence structures be used to detect AI use.

## Dataset
we will use the PubMed API to download a large number of articles from 2010-2015. In this time period AI was not used for writing, so we know all of these articles are written by humans. The PubMed API allows us to get any amount of articles identifiers in that time range. And then we can use the same API to download the articles in XML format with a lot of metadata. For now we only care about the actual text in the articles, so we'll have to do some formatting and text extraction. 

For our purposes it doesn't really matter if all of the articles are in the same field or not, so this approach will suffice. 

## Features
The model will look at a variety of features. Ideally we pick as many as possible to see which features carry most signal. Some featurse we can consider adding include:
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

Inclass Presentations - May 19/22
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

## Documentation

- **`AI_ACCESS.pdf`**: setup guide for calling Gemini through our shared Google Cloud project.

