# Helper functions
import os
from dotenv import load_dotenv

def get_api_key():
    """
    Gets the OpenAI API Key from environment.

    Returns:
        (str) : OpenAI API Key
    """
    load_dotenv("openai_api_key.env")

    return os.getenv("OPENAI_API_KEY")