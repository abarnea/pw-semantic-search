# Helper functions
import os
import pickle
from gensim.models import Word2Vec
from dotenv import load_dotenv

import doc_reader as reader
import md_cleaner as cleaner
import md_preprocessor as preprocessor

def get_api_key():
    """
    Gets the OpenAI API Key from environment.

    Returns:
        (str) : OpenAI API Key
    """
    load_dotenv("openai_api_key.env")

    return os.getenv("OPENAI_API_KEY")

def read_clean_process_data(docs: str) -> dict:
    """
    Read, clean, and process data
    """
    if not os.path.exists(docs):
        raise FileNotFoundError

    doc_data = reader.collect_doc_data(docs)
    cleaned_doc_data = cleaner.clean_doc_data(doc_data)
    preproc_docs = preprocessor.preprocess_doc_data(cleaned_doc_data)

    return preproc_docs

def clean_and_preproc_data(input_data):
    """
    Helper function to combine cleaning and preprocessing of data.

    Parameters:
        doc_data (dict | str) : raw documentation data or string

    Returns:
        cp_doc_data (dict | str) : cleaned and preprocessed doc data or string
    """
    if isinstance(input_data, dict):
        cleaned_data = cleaner.clean_doc_data(input_data)
        cp_data = preprocessor.preprocess_doc_data(cleaned_data)
    elif isinstance(input_data, str):
        cleaned_data = cleaner.clean_str(input_data)
        cp_data = preprocessor.preprocess_str(cleaned_data)

    return cp_data

def load_w2v(model_path="word2vec_model.bin"):
    """
    Loads Word2Vec model.
    """
    return Word2Vec.load(model_path)

def load_tfidf(vectorizer_path="tfidf_vectorizer.pkl",
               matrix_path="tfidf_matrix.pkl"):
    """
    Loads tfidx matrix and vectorizer.
    """
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)

    with open(matrix_path, 'rb') as f:
        tfidx_matrix = pickle.load(f)

    return vectorizer, tfidx_matrix