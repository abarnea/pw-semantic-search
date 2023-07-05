import numpy as np
import scipy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import md_cleaner as cleaner
import md_preprocessor as preprocessor
import helper_funcs as helper


def semantic_search(query: str,
                    preproc_docs: dict,
                    vectorizer: TfidfVectorizer,
                    tfidf_matrix: scipy.sparse.csr_matrix) -> list[str]:
    """
    Runs a semantic search with a query on inputted docs based on the TF-IDF
    model for numerical representation of words

    Parameters
    -----------
        query (str): the query string
        preproc_docs (dict): preprocessed documents, keyed by filename with
                values corresponding to the file content in tokenized form
        vectorizer (TfidfVectorizer): The initialized TF-IDF vectorizer
        tfidf_matrix (scipy.sparse.csr_matrix): The TF-IDF matrix

    Returns
    -----------
        results (list): List of tuples containing similar documents and their similarity scores
    """
    corrected_query = cleaner.correct_spelling(query)
    cp_query = helper.clean_and_preproc_data(corrected_query)
    query_vector = vectorizer.transform([" ".join(cp_query)])
    
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix)
    sorted_indexes = np.argsort(similarity_scores, axis=1)[0][::-1]

    filenames = list(preproc_docs.keys())
    similar_docs = [(filenames[i], similarity_scores[0][i]) for i in sorted_indexes]

    return similar_docs

def get_relevant_files(query: str,
                       preproc_docs: dict,
                       vectorizer: TfidfVectorizer,
                       tfidf_matrix: scipy.sparse.csr_matrix,
                       top_k=5,
                       include_score=False,
                       verbose=False) -> list[str]:
    """
    Gets the top 'k' relevant files from an inputted query. Defaults to top
    5 most relevant files.

    Parameters
    -----------
        query (str) : question to search PW documentation for
                preproc_docs (dict): preprocessed documents, keyed by filename with
                values corresponding to the file content in tokenized form
        vectorizer (TfidfVectorizer): The initialized TF-IDF vectorizer
        tfidf_matrix (scipy.sparse.csr_matrix): The TF-IDF matrix
        top_k (int) : top 'k' most relevant files to return (default: 5)
        include_score (bool) : if True, includes similarity score of file
        verbose (bool) : if True, prints files in addition to returning

    Returns
    -----------
        rel_files (list) : top 'k' most relevant files
    """
    try:
        similar_docs = semantic_search(query, preproc_docs, vectorizer, tfidf_matrix)
    except TypeError:
        print("Your query does not match anything in our system.")
        return []

    if include_score:
        rel_files = similar_docs[:top_k]
        if verbose:
            print(f"Top {top_k} most relevant files to your query with similarity scores included:\n")
            for i, (file, sim_score) in enumerate(rel_files):
                print(f"{i + 1}. {file}: {sim_score}")
        return rel_files
    else:
        rel_files = [filename for filename, _ in similar_docs[:top_k]]
        if verbose:
            print(f"Top {top_k} most relevant files to your query:\n")
            for i, file in enumerate(rel_files):
                print(f"{i + 1}. {file}")

    return rel_files