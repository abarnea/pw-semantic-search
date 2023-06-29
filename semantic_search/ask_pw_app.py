import subprocess
import streamlit as st

def main():
    st.title("Ask Parallel Works")

    st.markdown("The purpose of this platform is to assist users in understanding and navigating the Parallel Works (PW) platform. Questions can cover anything that is currently documented in the Parallel Works documentation, which can be found [here](https://docs.parallel.works/).")

    query = st.text_input("Enter your query:")

    if st.button("Ask"):
        if query:
            run_script(query)
        else:
            st.error("Error: No query provided.")

def run_script(query: str):
    """
    Runs the Ask Parallel Works script in Streamlit.

    Parameters
    -----------
        query (str) : user query to answer

    Returns
    -----------
        (Does not return a value)
    """
    command = ["bash", "ask_pw.sh", query]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = process.communicate()
    output = output.decode("utf-8")

    st.subheader("Answer:")
    st.write(output)

    if error:
        st.subheader("Script Error")
        st.error(error.decode("utf-8"))

if __name__ == "__main__":
    main()
