import gensim
import gensim.downloader
from gensim.models import Word2Vec
from gensim.matutils import unitvec
import numpy as np

import md_cleaner as cleaner
import md_preprocessor as preprocessor
import helper_funcs as helper


def create_doc_embeddings(preproc_docs: dict, model: object) -> dict:
    """
    Create document embeddings by averaging the word embeddings of the tokens
    of the preprocessed docs which are present in the model.

    Parameters
    -----------
        preproc_docs (dict): preprocessed documents, keyed by filename with
                values corresponding to the file content in tokenized form
        model: the trained Word2Vec model

    Returns
    -----------
        document_embeddings (dict): document embeddings dictionary keyed by
            filename with values corresponding to the document embeddings
    """
    document_embeddings = {}

    for filename, tokens in preproc_docs.items():
        embeddings = [model.wv[word] for word in tokens if word in model.wv]
        if embeddings:
            document_embeddings[filename] = unitvec(np.mean(embeddings, axis=0))

    return document_embeddings

def run_query(query_str: str, preproc_docs: dict, model: object) -> list[str]:
    """
    Performs a similarity search on the inputted query against a dictionary
    of preprocessed documents and an inputted Word2Vec model.

    Parameters
    -----------
        query_str (str) : user query
        preproc_docs (dict): preprocessed documents, keyed by filename with
                values corresponding to the file content in tokenized form
        model (object) : the trained Word2Vec model
    
    Returns
    -----------
        similar_docs (list[str]) : filenames of the most similar docs to the query
    """
    corrected_query = cleaner.correct_spelling(query_str)
    query_tokens = helper.clean_and_preproc_data(corrected_query)
    average_vec_rep = [model.wv[token] for token in query_tokens if token in model.wv]
    query_embedding = unitvec(np.mean(average_vec_rep, axis=0))

    doc_embeddings = create_doc_embeddings(preproc_docs, model)

    similar_docs = []
    for filename, doc_embedding in doc_embeddings.items():
        similarity_score = np.dot(doc_embedding, query_embedding)
        similar_docs.append((filename, similarity_score))
    
    similar_docs = sorted(similar_docs, key=lambda x: x[1], reverse=True)

    return similar_docs

def get_relevant_files(query: str, preproc_docs: dict, model: object, top_k=5, include_score=False, verbose=False) -> list[str]:
    """
    Gets the top 'k' relevant files from an inputted query. Defaults to top
    5 most relevant files.

    Parameters:
        query (str) : question to search PW documentation for
        preproc_docs (dict): preprocessed documents, keyed by filename with
                values corresponding to the file content in tokenized form
        model (object) : the trained Word2Vec model
        top_k (int) : top 'k' most relevant files to return (default: 5)
        include_score (bool) : if True, includes similarity score of file
        verbose (bool) : if True, prints files in addition to returning

    Returns:
        rel_files (list) : top 'k' most relevant files
    """
    try:
        similar_docs = run_query(query, preproc_docs, model)
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