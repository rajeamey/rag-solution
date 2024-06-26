"""
Streamlit App for Demonstrating Interactive RAG Solution

This script initializes a Streamlit app that which provide an interactive way for 
playing with RAG Solution.

Usage:
    Make sure you add OPENAI API key in PERSONAL_OPENAI_KEY environment variable.
    Also check path for data folder(DATA_FOLDER) provided.

    Run this script in conda env cli:
        streamlit run interactive-rag-solution.py

Author: Ameya Raje

"""

import streamlit as st
from utils import *

# data folder path
DATA_FOLDER: str = 'data'

st.title("Interactive LLM Desk")

st.text("NOTE:")
st.caption("1. Make sure you have provided valid OPENAI key in environment variables for 'PERSONAL_OPENAI_KEY'")
st.caption("2. Provide correct path to data folder. default path is `data`")
st.caption("3. Reloading will reinitialize generated indices of input data and RAG client")

# initialize and store RAGSolution object in streamlit session
if "rag_solution" not in st.session_state:
    # add loading spinner till object is initialized
    with st.spinner("Please wait till processing of data completes"):
        # set object in session
        st.session_state.rag_solution = RAGSolution(
            data_folder=DATA_FOLDER
        )

if "rag_solution" in st.session_state:
    st.write("`Great! RAG client is now active.`")
    # input box for question/query
    question: str = st.text_input("Please enter your question here!")

    # on submit action, process question
    if st.button("Submit"):
        if question:
            with st.spinner("Processing..."):
                # generate response from llm
                llm_response: str = st.session_state.rag_solution.generate_response(
                    question=question
                )
            # display received response
            st.write(llm_response)
        else:
            st.write("Please enter a question")