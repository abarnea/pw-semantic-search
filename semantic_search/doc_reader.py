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
        html = markdown.markdown(content)
        text = ''.join(BeautifulSoup(html).findAll(text=True))

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
                text = read_md_file(file_path)
                doc_data[file] = text
    
    return doc_data
