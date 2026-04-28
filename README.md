# Project Readme

## Title
Are we cooked chat?: General text characteristics in Human and AI Writing

## Abstract
The introduction of Large Language Models (LLMs) has raised questions about their influence in human language. This influence can occur directly through users copying the output of an LLM, or indirectly through humans mirroring the language usage by LLMs. Current research focuses on analyzing the frequency of certain words like “delve” and “align”, given that LLMs use these disproportionately often. Going beyond this, in this research we will investigate whether, similarly to the increase of specific vocabulary, certain other characteristics have also increased. Specifically, we will look at the following 4 characteristics:
- Average sentence length
- Average word length
- Number of nouns
- Number of verbs
With gender studies papers published between 2015-2020, we'll use LLM's to rewrite these papers and creata a generated counterpart. Between these two dataset we'll then analyse the evolution of these characterisitcs, highlighting correlations with AI use. We'll use a webscraper to collect the papers.

## Research questions
- How have the 4 characteristics changed over time in the field of gender studies?
- Is there a correlation between the use of LLMs and the values of the 4 characteristics?    
- (discussion) To what extent can the prevalence of “AI characteristic” vocabulary and sentence structures be used to detect AI use.

## Dataset
We'll first manually collect papers in the field of gender studies, being published between 2015-2020, to gather some examples for the webscraper. Then we'll use this webscraper to generate the full data set of papers. Since all these papers were published before the release and widespread use of generative AI, they serve as a good baseline for non-AI generated papers. We will be including the full texts of English papers withing the field of gender studies, of which we'll count the average sentence lenght, average word length, number of nouns, and number of verbs. Since we're rewriting the same papers using LLM's, we're able to make a straight comparison between the original and the generated papers, allowing for us to make clear correlations between AI use and the evolution of these characteristics.

## A Tentative List of Milestones
Project Update 0 - April 14
- Repository and README [Everyone]

Project Update 1 - April 28
- Update README to newer goals, in relation to lack of antitheses found [Melle]
- Write model fitting code [Wout]
- Find final dataset [Jonathan]
- Decides on tests run:
- Find 20 base sources [Lettie & Melle]
- What amount (& dataset breakdown: ie x papers separated into y academic fields and z years) [Melle]
- Create generated papers pipeline [Jonathan]

Project Update 2 - May 8
- Have a webscraper to collect articles in the field of gender studies [Wout]
- Have a full dataset of 1000 papers in genderstudies published between 2015-2020 and written in English [Melle]
- Run models on the full dataset and gather results [Melle & Leticia]
- Analyze results and create base for the report [Jonathan]

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
This can be added as the project unfolds. You should describe, in particular, what your repo contains and how to reproduce your results.

- **`AI_ACCESS.pdf`**: setup guide for calling Gemini through our shared Google Cloud project (`auc-text-mining-antithesis`). Each group member should follow these steps once before running anything that uses the Gemini API.
