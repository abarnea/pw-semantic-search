# Overview

This file is meant to provide an overview of the project, useful tools I've found during research, and any notes that I have about the project as I move forward.

## Project Description: Implement Q&A against documentation with semantic search and ChatGPT

### Introduction to the Project

We're looking to create a prototype of a workflow that would answer a given question (i.e. Q&A). We can do so with the following steps (courtesy of Alvaro):

1. Clone https://github.com/parallelworks/docs 
2. Run a semantic search on our documentation to find which `.md`/`.mdx` files are relevant to answer a given question.
3. Glue these files together and pass them to the ChatGPT API together with the question 
​
Alvaro believes that step 2, finding the relevant files, will be the most difficult. Step 1 is trivial, of course, and step 3 has a plethora of examples to pull from. Step 2, i.e. the semantic search, would be good to have as a resource on its own.

### Notes from Michael:

Based on Alvaro's comments, the project is based on two different steps:

1. Semantic Analysis to create a prompt to query.
2. Querying the model with the crafted/augmented prompt.

Michael suggests exploring the Azure AI Studio since we'll effectivelyl have to feed in a processed version of Parallel Works documentation and have the AI learn from it. This also provides a "low-code" solution that we could explore first before trying a custom solution.


## Useful Python libraries for implementing semantic search

### For analyzing data from `.md` files in the Github repo:

**Markdown**: Reads the content of `.md` files and extracts the text data into plain text for analysis

### For actual semantic search:

**NLTK**: Provides tools for natural language processing, such as tokenization, stemming, and lemmatization.

**Gensim**: Offers implementations of various word embedding models like Word2Vec and GloVe.

**Scikit-learn**: Provides methods for feature extraction and vectorization, such as TF-IDF.

**Annoy**: A library for approximate nearest neighbor search, which can be useful for efficient indexing and retrieval.

## Useful links from Michael:

**Vercel AI SDK**: https://vercel.com/blog/introducing-the-vercel-ai-sdk

**Implementing a GPT-powered Chatbot**: https://github.com/vercel/examples/tree/main/solutions/ai-chatgpt

**GPT-3 Chatbot Example**: https://vercel.com/templates/next.js/ai-gpt3-chatbot

**Azure AI Studio**: https://youtu.be/DaIYrlMOj7I