import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

def tokenize_str(input_str: str) -> list[str]:
    """
    Tokenizes an input string. Tokenization is the process of splitting a string
    into a list of word "tokens", i.e. into each separate word component of the
    original string.

    Parameters
    -----------
        input_str (str) : inputed string to tokenize

    Returns
    -----------
        (list[str]) : tokenized input string
    """
    return word_tokenize(input_str)

def _remove_stopwords(tokens: list[str]) -> list[str]:
    """
    Remove stop-words from a list of string tokens, such as "the", "at", etc.

    Parameters
    -----------
        tokens (list[str]) : list of string word tokens

    Returns
    -----------
        (list[str]) : tokenized string with stopwords removed
    """
    stop_words = set(stopwords.words('english'))
    return [token for token in tokens if token not in stop_words]

def _stem_tokens(tokens: list[str]) -> list[str]:
    """
    Stems a list of string tokens. Stemming is the process of reducing inflected
    words to their word stem, or base/root form. For example, "running" and
    "runs" would just become "run".

    Parameters
    -----------
        tokens (list[str]) : list of string word tokens

    Returns
    -----------
        (list[str]) : tokenized string with words stemmed
    """
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]

def _lemmatize_tokens(tokens: list[str]) -> list[str]:
    """
    Lemmatizes a list of string tokens. Lemmatization is the process of grouping
    inflected forms together as a single base form. For example, "builds",
    "built", "building", etc. all become "build".

    Parameters
    -----------
        tokens (list[str]) : list of string word tokens

    Returns
    -----------
        (list[str]) : tokenized string with words lemmatized
    """
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]

def _clean_tokens(tokens: list[str]) -> list[str]:
    """
    Removes punctuation and special characters from a list of strings.

    Parameters
    -----------
        tokens (list[str]) : inputted token string

    Returns
    -----------
        (list[str]) : tokenized string with only alphanumeric characters
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
    nltk.download("punkt")
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