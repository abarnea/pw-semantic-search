import sys
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

import doc_reader as reader
import md_cleaner as cleaner
import md_preprocessor as preprocessor
import helper_funcs as helper

SUPER_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(SUPER_PATH, "data")
MODEL_PATH = os.path.join(SUPER_PATH, "models")

def initialize_vectorizer(docs):
    """
    Initializes a TF-IDF vectorizer model on inputted documents.
    """
    preproc_docs = helper.read_clean_process_data(docs)

    vectorizer = TfidfVectorizer(sublinear_tf=True, stop_words='english')

    tokenized_corpus = list(preproc_docs.values())
    corpus = [' '.join(tokens) for tokens in tokenized_corpus]

    tfidf_matrix = vectorizer.fit_transform(corpus)

    return vectorizer, tfidf_matrix

if __name__ == "__main__":
    input_docs_path = sys.argv[1] if len(sys.argv) >= 2 else "docs"
    docs_path = os.path.join(DATA_PATH, input_docs_path)
    vectorizer, tfidf_matrix = initialize_vectorizer(docs_path)

    with open(os.path.join(MODEL_PATH, "tfidf_vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)

    with open(os.path.join(MODEL_PATH, "tfidf_matrix.pkl"), "wb") as f:
        pickle.dump(tfidf_matrix, f)
