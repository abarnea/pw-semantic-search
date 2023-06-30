#!/bin/bash

if [ "$1" = "-u" ]
then
    echo "Deleting existing 'docs' directory..."
    rm -rf docs
    echo "Cloning Parallel Works documentation from GitHub..."
    git clone https://github.com/parallelworks/docs
    echo "Parallel Works documentation cloned successfully!"
    shift
fi

if [ -z "$1" ] && [ ! -d "docs" ]
then
    echo "Warning: Parallel Works documentation folder not found. Please specify the path for the PW docs to train the models."
    exit 1
fi

if [ ! -f "word2vec_model.bin" ]
then
    echo "word2vec_model.bin not found. Creating Word2Vec model..."
    if [ -z "$1" ]
    then
        python3 create_w2v_model.py
    else
        python3 create_w2v_model.py "$1"
    fi
    echo "Word2Vec model created successfully!"
else
    echo "word2vec_model.bin already exists. Skipping Word2Vec model creation."
fi

if [ ! -f "tfidf_vectorizer.pkl" ] || [ ! -f "tfidf_matrix.pkl" ]
then
    echo "tfidf_vectorizer.pkl or tfidf_matrix.pkl not found. Creating TF-IDF models..."
    if [ -z "$1" ]
    then
        python3 create_tfidf_model.py
    else
        python3 create_tfidf_model.py "$1"
    fi
    echo "TF-IDF model created successfully!"
else
    echo "Both tfidf_vectorizer.pkl and tfidf_matrix.pkl exist. Skipping TF-IDF model creation."
fi