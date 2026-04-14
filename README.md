# Project Readme

## Title
Are we cooked: Sentence structures in human and AI writing

## Abstract
A max 150-word description of the project question or idea, goals, dataset used. What story would you like to tell and why? What's the motivation behind your project?

The introduction of Large Language Models (LLMs) has raised questions about their influence in human language. This influence can occur directly through users copying the output of an LLM, or indirectly through humans mirroring the language usage by LLMs. Current research focuses on analyzing the frequency of certain words like “delve” and “align”, given that LLMs use these disproportionately often. Going beyond this, in this research we will investigate whether, similarly to the increase of specific vocabulary, certain sentence structures are used more frequently since the widespread adoption of LLMs. Specifically, we will look at the antithesis, where in a single sentence two opposing ideas are introduced for a contrasting effect. Using the arXiv dataset, we will extract multiple scientific texts to determine if there is a correlation between the use of this antithesis structure and the increasing use of LLMs.

## Research questions
A list of research questions you would like to address during the project. 
- Is there a correlation between the use of LLMs and the frequency of the antithesis is writing and speaking? 
- Which scientific fields have seen a bigger increase in the use of the antithesis since the launch of LLMs? 
- Which discourse types (news articles, reddit comments, scientific articles etc) have seen a bigger increase in the use of the antithesis? 
- What are characteristic sentence structures (CSS) generally used by generative AI? 
- (discussion) To what extent can the prevalence of “AI characteristic” vocabulary and sentence structures be used to detect AI use.

## Dataset
List the dataset(s) you want to use, and some ideas on how you expect to get, manage, process and enrich it/them. Show you've read the docs and are familiar with some examples, and you've a clear idea on what to expect. Discuss data size and format if relevant.:

We use the arXiv dataset, taking the full text of each paper. We focus on English papers from a few years before and after the ChatGPT release, sampled evenly across fields rather than using everything published. We will have to clean the text of irrelevant elements (ie latex formatting, page numbers, works cited, etc). From each paper we pull two things: vocabulary features (lemma frequencies, type-token ratios, and rates for a curated list of suspected AI-tell words like delve, tapestry, intricate and multifaceted) and construction features (a parser pass that flags the "it's not X, it's Y" family).


## A tentative list of milestones for the project
Add here a sketch of your planning for the coming weeks. Please mention who does what.

Deadlines:

[Assign your roles here]
Project Update 0 - April 14
Repository and README [Everyone]

Project Update 1 - April 28
Decide on CSS/AI determining structures, based on literature [Melle]
Decide on model and have it tested on preliminary dataset [Wout]
Find final dataset [Jonathan]
Decides on tests run:
What time frame (Texts published from when to when)
What academic fields (Computer Science, Chemistry, Politics…)
What sources (Academic papers and from where)
What amount (& dataset breakdown: ie x papers separated into y academic fields and z years)
Data gathering and preprocessing pipeline [Melle]

Project Update 2 - May 8
Run models on the full dataset and gather results[Melle & Leticia]
Analyze results and create base for the report [Jonathan]

Inclass Presentations - May 19/22
Presentation prepared [Everyone]
First draft of the report done
Abstract [Jonathan]
Introduction [Leticia] 
Related work
Data collection
Dataset description with summary statistics
Methods with math and description of main algorithms [Leticia &...]
Results and findings [Jonathan]
Conclusions [Jonathan]

Final Deadline - May 22
Implement feedback to report and code
Clean up the repository and the report

## Documentation
This can be added as the project unfolds. You should describe, in particular, what your repo contains and how to reproduce your results.
