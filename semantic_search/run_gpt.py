import sys
import json
import openai
from semantic_search import semsearch
import helper_funcs as helper

def format_gpt_input(gpt_docs: dict) -> dict:
    """
    Formats the documentation to be passed into ChatGPT API into a joined
    sentence structure to minimize GPT API token input.

    Parameters
    -----------
        gpt_docs (dict) : Formatted documentation to be inputted into ChatGPT API

    Returns
    -----------
        gpt_input (dict) : dictionary keyed by the same filenames, but the
                the content is now strings instead of lists of string tokens
    """

    return {file : " ".join(content) for file, content in gpt_docs.items()}

def run_gpt(query, *args, api_key=helper.get_api_key()):
    """
    Function that runs the gpt-3.5-turbo AI API on a query and set of arguments
    Arguments should consist of a variable length list, where each
    element contains a list of tokens from the most relevant files related to
    the inputted query.

    Paramaters:
        query (str) : inputted query from user
        *args (list[list[str]]) : array containing document information tokens
        api_key (str) : user API key to run
    
    Returns:
        reply (str) : GPT AI response to query with supporting relevant documents
    """
    openai.api_key = api_key

    gpt_prompt = "You are a helpful assistant in charge of helping users understand our platform."
    clarification_1 = "Your responses should not require users to search through our files. Instead, you can include relevant filenames as additional support resources if they need it."
    clarification_2 = "When telling a user to navigate to a documentation page in your response, print the file name in Proper formatting without dashes or file extensions."
    clarification_3 = "If the inputted query does not seem related to the PW documentation, respond to the user explaining that you are meant as an assistant for the Parallel Works platform."

    messages = [
        {"role": "system", "content": gpt_prompt},
        {"role": "system", "content": clarification_1},
        {"role": "system", "content": clarification_2},
        {"role": "system", "content": clarification_3},
        {"role": "user", "content": query}
    ]

    for tokens in args:
        messages.append({"role": "user", "content": json.dumps(tokens)})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    reply = response.choices[0].message.content
    return reply

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Query input required.")

    query = sys.argv[1]

    docs_path = sys.argv[2] if len(sys.argv) >= 3 else "docs/docs"
    preproc_docs = helper.read_clean_process_data(docs_path)

    w2v_model = helper.load_w2v()
    vectorizer, tfidf_matrix = helper.load_tfidf()

    ss_docs = semsearch(query, preproc_docs, w2v_model, vectorizer, tfidf_matrix)

    gpt_args = format_gpt_input(ss_docs)

    reply = run_gpt(query, gpt_args)

    print(f"\n{query}\n\n{reply}\n")

