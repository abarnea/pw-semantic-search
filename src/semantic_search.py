import w2v_semantic_search as w2v
import tfidf_semantic_search as tfidf

def get_common_files(w2v_output: list[str], tfidf_output: list[str]) -> list[str]:
    """
    Gets the common file names between two lists

    Parameters
    -----------
        w2v_output (list[str]) : list of file names from Word2Vec model
        tfidf_output (list[str]) : list of file names from TF_IDF model

    Returns
    -----------
        common_files (list[str]) : the common file names from the two inputted
                models if there are any in common, otherwise takes the top three
                files from the Word2Vec model output.
    """

    common_files = list(set(w2v_output).intersection(tfidf_output))

    return common_files if common_files != [] else w2v_output[:3]

def get_file_content_from_filenames(filenames: list, docs: dict) -> dict:
    """
    Helper function that takes a list of filenames and returns a list of
    the cleaned and preprocessed contents of those files.

    Parameters
    -----------
        filenames (list) : filenames to get content of
        docs (dict) : documents keyed by filename and valued with content

    Returns:
        file_content (dict) : content of each of the inputted filenames
    """
    return {file: docs[file] for file in filenames}

def semsearch(query,
              preproc_docs,
              w2v_model,
              top_k=5,
              include_score=False,
              verbose=False):
    """
    Overall semantic search function which takes in a query, preprocessed
    documentation, a Word2Vec model, a TF-IDF vectorizer and matrix, and optional
    parameters for file processing, and outputs the common filenames and the content
    of those files between the two models after conducting a semantic search based
    on the query through trained Word2Vec and TF-IDF models on the documentation.

    Parameters
    -----------
        query (str) : Inputted user question
        preproc_docs (dict) : preprocessed documentation
        w2v_model : pre-trained Word2Vec model
        vectorizer : pre-trained TF-IDF model vectorizer
        tfidf_matrix : pre-trained TF-IDF model matrix
        top_k (int) : top 'k' most relevant files to return (default: 5)
        include_score (bool) : if True, includes similarity score of file
        verbose (bool) : if True, prints files in addition to returning

    Returns
    -----------
        common_content (dict) : the top_k most relevant files, keyed by filename
            and corresponding to the content of those respective docs
    """
    w2v_output = w2v.get_relevant_files(query,
                                        preproc_docs,
                                        w2v_model,
                                        top_k=top_k,
                                        include_score=include_score,
                                        verbose=verbose)

    # tfidf_output = tfidf.get_relevant_files(query,
    #                                         preproc_docs,
    #                                         vectorizer,
    #                                         tfidf_matrix,
    #                                         top_k=top_k,
    #                                         include_score=include_score,
    #                                         verbose=verbose)

    # common_files = get_common_files(w2v_output, tfidf_output)

    w2v_content = get_file_content_from_filenames(w2v_output, preproc_docs)

    return w2v_content