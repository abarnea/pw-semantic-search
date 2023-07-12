import subprocess
import streamlit as st
import json
import os

QUERIES_PATH = "queries.json"

def main():
    st.title("Ask Parallel Works")

    intro_message = "The purpose of this platform is to assist users in understanding and navigating the Parallel Works (PW) platform. Questions can cover anything that is currently documented in the Parallel Works documentation, which can be found [here](https://docs.parallel.works/)."

    st.markdown(intro_message)

    query = st.text_input("Enter your query:")

    if st.button("Ask"):
        if query:
            with st.spinner("Processing..."):
                answer = run_script(query)
            save_query(query, answer)
        else:
            st.error("Error: No query provided.")

    queries = load_queries()
    display_sidebar(queries)

def run_script(query: str):
    """
    Runs the Ask Parallel Works script in Streamlit.

    Parameters
    -----------
        query (str) : user query to answer

    Returns
    -----------
        output (str) : run_gpt output
    """
    command = ["bash", "ask_pw.sh", query]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = process.communicate()
    output = output.decode("utf-8")

    st.subheader("Answer:")

    if error:
        st.subheader("Script Error")
        st.error(error.decode("utf-8"))

    st.write(output)

    return output

def save_query(query: str, answer: str):
    """
    Saves the query and answer to a JSON file.

    Parameters
    -----------
        query (str) : user query
        answer (str) : answer to the query

    Returns
    -----------
        (Does not return a value)
    """
    queries = load_queries()
    queries[query] = answer

    with open(QUERIES_PATH, "w") as f:
        json.dump(queries, f)

def load_queries():
    """
    Loads the queries from the JSON file.

    Returns
    -----------
        queries (dict) : dictionary of query-answer pairs
    """
    try:
        with open(QUERIES_PATH, "r") as f:
            queries = json.load(f)
    except FileNotFoundError:
        queries = {}

    return queries

def display_sidebar(queries: dict):
    """
    Displays the sidebar for Streamlit

    Parameters
    -----------
        queries (dict) : dictionary containing user queries and answers

    Returns
    -----------
        (Does not return a value)
    """
    st.sidebar.title("Previous Queries")

    rev_queries = list(queries.items())[::-1]
    num_queries = len(rev_queries)

    for i, (query, answer) in enumerate(rev_queries):
        query_expander = st.sidebar.expander(f"Query {num_queries - i}: {query}")
        with query_expander:
            st.write(answer)

    if os.path.isfile(QUERIES_PATH):
        clear_button = st.sidebar.button("Clear Queries")
        if clear_button:
            subprocess.run(["rm", "-f", QUERIES_PATH])

if __name__ == "__main__":
    main()
