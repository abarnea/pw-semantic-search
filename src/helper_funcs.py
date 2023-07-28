# Helper functions
import os
import pickle
import nltk
from gensim.models import Word2Vec
from dotenv import load_dotenv

import doc_reader as reader
import md_cleaner as cleaner
import md_preprocessor as preprocessor

SUPER_PATH = "../models/"

def get_api_key():
    """
    Gets the OpenAI API Key from environment.

    Returns:
        (str) : OpenAI API Key
    """
    env_file = "openai_api_key.env"

    if os.path.exists(env_file):
        load_dotenv("openai_api_key.env")

    return os.getenv("OPENAI_API_KEY")

def read_clean_process_data(docs: str) -> dict:
    """
    Reads, cleans, and processes input documentation data using the doc_reader,
    md_cleaner, and md_preprocessor stages.

    Parameters
    -----------
        docs (str) : path to documentation folder

    Returns
    -----------
        preproc_docs (dict) : cleaned and preprocessed documentation data
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

def load_w2v(model_path=SUPER_PATH + "word2vec_model.bin"):
    """
    Loads the Word2Vec model from a stored file.

    Parameters:
        model_path (str): Path to the Word2Vec model file (default: "word2vec_model.bin")

    Returns:
        (object) : Word2Vec model object
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"The Word2Vec model file '{model_path}' does not exist.")

    return Word2Vec.load(model_path)

def load_tfidf(vectorizer_path=SUPER_PATH + "tfidf_vectorizer.pkl",
               matrix_path=SUPER_PATH + "tfidf_matrix.pkl"):
    """
    Loads the TF-IDF model vectorizer and matrix from stored files.

    Parameters:
        vectorizer_path (str): Path to the TF-IDF vectorizer file (default: "tfidf_vectorizer.pkl").
        matrix_path (str): Path to the TF-IDF matrix file (default: "tfidf_matrix.pkl").

    Returns:
        vectorizer (object): TF-IDF vectorizer object
        tfidf_matrix (object): TF-IDF matrix object
    """
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"The TF-IDF vectorizer file '{vectorizer_path}' does not exist.")

    if not os.path.exists(matrix_path):
        raise FileNotFoundError(f"The TF-IDF matrix file '{matrix_path}' does not exist.")

    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)

    with open(matrix_path, 'rb') as f:
        tfidf_matrix = pickle.load(f)

    return vectorizer, tfidf_matrix

def check_nltk_data():
    """
    Check and download necessary data for NLTK packages.
    """
    nltk_packages = ['punkt', 'stopwords', 'wordnet']

    for package in nltk_packages:
        try:
            nltk.data.find(f'corpora/{package}')
        except LookupError:
            print(f"Downloading '{package}' data...")
            nltk.download(package)
            print(f"'{package}' data downloaded successfully.")
        else:
            print(f"'{package}' data is already downloaded.")