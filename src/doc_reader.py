import os
import markdown
from bs4 import BeautifulSoup

def read_md_file(filepath: str) -> str:
    """
    Reads a markdown file and processes it into a string of plain text.

    Parameters:
        filepath (str) : the filepath of the markdown file to read
    
    Returns:
        text (str) : the plain text from the inputted markdown file
    """
    with open(filepath, 'r') as f:
        content = f.read()
        md_text =  markdown.markdown(content)
        text = ''.join(BeautifulSoup(md_text, features="html5lib").findAll(text=True))

    return text

def collect_doc_data(directory: str) -> list[str]:
    """
    Scans through a directory and collects the documentation data from all
    '.md' files into a list.

    Parameters:
        directory (str) : directory to scan through
    
    Returns
        docs_data (list[str]) : documentation data from `.md` files
    """
    doc_data = {}
    for dirpath, _, filenames in os.walk(directory):
        for file in filenames:
            if file.endswith('.md'):
                file_path = os.path.join(dirpath, file)
                content = read_md_file(file_path)
                proper_filename = convert_filename(file)
                doc_data[proper_filename] = content
    
    return doc_data

def create_hyperlink_dict(directory: str) -> dict:
    """
    Scans through a directory and creates a dictionary keyed by each file name
    with corresponding values being a created hyperlink for the PW page.

    Parameters:
        directory (str) : directory to scan through

    Returns
        hyperlinks (dict) : the hyperlinks corresponding to filenames
    """
    default_path = "https://docs.parallel.works/"
    hyperlinks = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_name = os.path.splitext(file)[0]
                subdirectories = os.path.relpath(root, directory)
                hyperlink = default_path + subdirectories + "/" + file_name
                proper_filename = convert_filename(file)
                hyperlinks[proper_filename] = hyperlink

    return hyperlinks

def convert_filename(filename):
    """
    Converts a filename in the form "file-template.md" into "File Template".

    Parameters:
        filename (str): the filename to convert

    Returns:
        converted_name (str): the converted filename
    """
    name_parts = filename.split("-")
    name_parts = [part.capitalize() for part in name_parts]
    converted_name = " ".join(name_parts).replace(".md", "")

    return converted_name
