# RAG Solution

This repository contains an implementation of a Retrieval-Augmented Generation (RAG) solution.
It uses OpenAI's GPT-3.5 and FAISS for efficient similarity search. Streamlit for creating interactive data applications.
Jupyter notebook is also present for use.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Features

- Efficient document retrieval using FAISS.
- Response generation using OpenAI's GPT-3.5.
- Streamlit app for interactive query input and response display.

## Installation

### Prerequisites

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) should be installed on your system.
- An OpenAI API key. Set it as an environment variable: `PERSONAL_OPENAI_KEY`.

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/rajeamey/rag-solution.git
    cd rag-solution
    ```

2. Create and activate the Conda environment:

    ```bash
    conda env create -f environment.yml
    conda activate rag-solution
    ```

3. Set up environment variables:

    ```bash
    export PERSONAL_OPENAI_KEY='your_openai_api_key'
    ```

## Usage

### Interactive Streamlit App

1. Place your data files (text files) in the `data` folder.

2. Run the Streamlit app:

    ```bash
    streamlit run interactive-rag-solution.py
    ```

3. Open your web browser and go to `http://localhost:8501` to interact with the app.

### Jupyter Notebook

1. Start Jupyter notebook:

    ```bash
    jupyter notebook
    ```

2. Open your web browser and go to `http://127.0.0.1:8888/tree?`

3. Open `rag-solution.ipynb`