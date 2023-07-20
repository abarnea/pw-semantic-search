import sys
import os
import gensim
import gensim.downloader
from gensim.models import Word2Vec
import numpy as np

import doc_reader as reader
import md_cleaner as cleaner
import md_preprocessor as preprocessor
import helper_funcs as helper

SUPER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_model(docs: dict, add_train_data=True):
    """
    Creates a Word2Vec model based on a Wiki News pretrained vectorized model
    and a provided dictionary of documentation.

    Parameters
    -----------
        docs (dict) : input docs in format filename : content
        add_train_data (bool) : whether or not to add the training data from wiki news

    Returns
    -----------
        model (object) : Word2Vec model to be saved
    """

    preproc_docs = helper.read_clean_process_data(docs)

    corpus = list(preproc_docs.values())
    model = Word2Vec(corpus, vector_size=500, window=5, min_count=2, workers=4)

    if add_train_data:
        # googlenews_model = gensim.downloader.load('word2vec-google-news-300')
        # model.build_vocab_from_freq(googlenews_model.key_to_index, corpus_count=len(corpus), update=True)
        wikinews_model_path = os.path.join(SUPER_DIR, "data/wiki-news-300d-1M-subword.vec")
        wikinews_model = gensim.models.KeyedVectors.load_word2vec_format(wikinews_model_path, binary=False)
        model.build_vocab_from_freq(wikinews_model.key_to_index, corpus_count=len(corpus), update=True)

    return model

if __name__ == "__main__":
    input_docs_path = sys.argv[1] if len(sys.argv) >= 2 else "data/docs"
    docs_path = os.path.join(SUPER_DIR, input_docs_path)
    model = create_model(docs_path)
    model.save(os.path.join(SUPER_DIR, "models/word2vec_model.bin"))