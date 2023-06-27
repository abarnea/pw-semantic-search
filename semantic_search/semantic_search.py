import w2v_semantic_search as w2v
import tfidf_semantic_search as tfidf

def _get_common_files(w2v_output, tfidf_output):
    """
    Gets the common filenames between two lists.
    """
    common_files = list(set(w2v_output).intersection(tfidf_output))

    return common_files if common_files != [] else w2v_output[:3]

def get_file_content_from_filenames(filenames: list, docs: dict) -> list:
    """
    Helper function that takes a list of filenames and returns a list of
    the cleaned and preprocessed contents of those files.

    Parameters:
        filenames (list) : filenames to get content of
        docs (dict) : documents keyed by filename and valued with content

    Returns:
        file_content (list) : content of each of the inputted filenames
    """
    return {file: docs[file] for file in filenames}

def semsearch(query,
              preproc_docs,
              w2v_model,
              vectorizer,
              tfidf_matrix,
              top_k=5,
              include_score=False,
              verbose=False):
    """
    Overall semantic search function which takes in a query, preprocessed
    documentation, a Word2Vec model, a TF-IDF vectorizer and matrix, and optional
    parameters for file processing, and outputs the common filenames and the content
    of those files between the two models after conducting a semantic search based
    on the query through trained Word2Vec and TF-IDF models on the documentation.

    Parameters:
        query (str) : Inputted user question
        preproc_docs (dict) : preprocessed documentation
        w2v_model : pre-trained Word2Vec model
        vectorizer : pre-trained TF-IDF model vectorizer
        tfidf_matrix : pre-trained TF-IDF model matrix
        top_k (int) : top 'k' most relevant files to return (default: 5)
        include_score (bool) : if True, includes similarity score of file
        verbose (bool) : if True, prints files in addition to returning

    Returns:
        common_content (dict) : the top_k most relevant files, keyed by filename
            and corresponding to the content of those respective docs
    """
    w2v_output = w2v.get_relevant_files(query,
                                        preproc_docs,
                                        w2v_model,
                                        top_k=top_k,
                                        include_score=include_score,
                                        verbose=verbose)

    tfidf_output = tfidf.get_relevant_files(query,
                                            preproc_docs,
                                            vectorizer,
                                            tfidf_matrix,
                                            top_k=top_k,
                                            include_score=include_score,
                                            verbose=verbose)

    common_files = _get_common_files(w2v_output, tfidf_output)

    common_content = get_file_content_from_filenames(common_files, preproc_docs)

    return common_content