import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

def tokenize_str(input_str: str) -> str:
    """
    Tokenize an input string.
    """
    return word_tokenize(input_str)

def _remove_stopwords(tokens: list[str]) -> list[str]:
    """
    Remove stop-words from a list of tokens.
    """
    stop_words = set(stopwords.words('english'))
    return [token for token in tokens if token not in stop_words]

def _stem_tokens(tokens: list[str]) -> list[str]:
    """
    Stems tokens.
    """
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]

def _lemmatize_tokens(tokens: list[str]) -> list[str]:
    """
    Lemmatizes tokens.
    """
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]

def _clean_tokens(tokens: list[str]) -> list[str]:
    """
    Clean tokens again.
    """
    return [re.sub(r'[^a-zA-Z0-9]', '', token) for token in tokens if token]

def preprocess_str(cleaned_str: str) -> list[str]:
    """
    Helper function to preprocess an inputted string via tokenization, stemming or 
    lemmatizing, and stop-word removal.

    Parameters:
        cleaned_str (str) : a pre-cleaned string
    
    Returns:
        preproc_tokens (list[str]) : preprocessed tokens of a string
    """
    tokens = tokenize_str(cleaned_str)

    preproc_funcs = [_remove_stopwords, _lemmatize_tokens, _clean_tokens] 

    preproc_tokens = tokens
    for func in preproc_funcs:
        preproc_tokens = func(preproc_tokens)
    
    return preproc_tokens

def preprocess_doc_data(cleaned_doc_data: list[str]) -> list[list[str]]:
    """
    Preprocesses the full documentation data set by tokenizing each string entry
    in the inputted documentation data, then removing stop words and lemmatizing
    the tokens via the WordNetLemmatizer algorithm.

    Parameters:
        cleaned_doc_data (list[str]) : cleaned documentation data
    
    Returns:
        preproc_doc_data (list[list[str]]) : full pre-processed documentation data
    """
    return {file : preprocess_str(content) for file, content in cleaned_doc_data.items()}