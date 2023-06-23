import re
from spellchecker import SpellChecker
import md_preprocessor as preprocessor


def _remove_whitespace(input_str: str) -> str:
    """
    Removes whitespace from an input string.
    """
    return ' '.join(input_str.split())


def _lower_str(input_str: str) -> str:
    """
    Lowers the input string to lower case
    """
    return input_str.lower()


def _remove_punct_and_special_chars(input_str: str) -> str:
    """
    Removes punctuation and special characters using Regex
    """
    pattern = r'[^\w\s]'
    return re.sub(pattern, '', input_str)


def _filter_sidebar_pos(input_str: str) -> str:
    """
    Removes sidebar positioning.
    """
    pattern = r"sidebar_position(?: \d+)? "
    return re.sub(pattern, "", input_str)


def clean_str(input_str: str) -> str:
    """
    Applies data cleaning measures to input string, including removing whitespaces,
    lowercasing the string, removing punctuations and special characters, and
    filtering sidebar positioning from .md files.

    Parameters:
        input_str (str) : inputted string to be cleaned
    
    Returns:
        cleaned_str (str) : cleaned string
    """
    cleaning_funcs = [_remove_whitespace,
                      _lower_str,
                      _remove_punct_and_special_chars,
                      _filter_sidebar_pos]
    
    cleaned_str = input_str
    for func in cleaning_funcs:
        cleaned_str = func(cleaned_str)

    return cleaned_str


def clean_doc_data(doc_data: list[str]) -> list[str]:
    """
    Clean the documentation data by removing HTML tags, removing punctuation
    and special characters, removing extra whitespaces, making everything
    lowercase, and catching mispelled words.

    Parameters:
        doc_data (list[str]) : the collected and read `.md` data
    
    Returns:
        cleaned_doc_data (list[str]) : the cleaned documentation data
    """
    return {file : clean_str(content) for file, content in doc_data.items()}


def correct_spelling(query_str):
    """
    Function to spell check a set of query tokens

    Parameters:
        query (str) : input string

    Returns:
        corrected_str (str) : corrected spelling for input string
    """
    spell = SpellChecker()
    query_tokens = preprocessor.word_tokenize(query_str)
    misspelled = spell.unknown(query_tokens)

    corrected_query = []
    for word in query_tokens:
        if word in misspelled:
            corrected_query.append(spell.correction(word))
        else:
            corrected_query.append(word)

    corrected_str = " ".join(corrected_query)

    return corrected_str
