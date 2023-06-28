#!/bin/bash

if [ -f "word2vec_model.bin" ]
then
    rm word2vec_model.bin
    rm word2vec_model.bin.syn1neg.npy
    rm word2vec_model.bin.wv.vectors.npy
    echo "word2vec_model.bin deleted successfully!"
else
    echo "word2vec_model.bin does not exist."
fi

if [ -f "tfidf_vectorizer.pkl" ]
then
    rm tfidf_vectorizer.pkl
    echo "tfidf_vectorizer.pkl deleted successfully!"
else
    echo "tfidf_vectorizer.pkl does not exist."
fi

if [ -f "tfidf_matrix.pkl" ]
then
    rm tfidf_matrix.pkl
    echo "tfidf_matrix.pkl deleted successfully!"
else
    echo "tfidf_matrix.pkl does not exist."
fi
