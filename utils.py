"""
Utility module for streamlit script.

This serves as a module in interactive-rag-solution script.

Author: Ameya Raje

"""

import faiss
import numpy as np
import os
import openai
import sqlite3

class RAGSolution:
    """
        This is entry class for this rag solution.

    """

    def __init__(self, data_folder: str):
        """
            init method for RAGSolution.
        """

        # check of env variables are set or not
        if "PERSONAL_OPENAI_KEY" not in os.environ:
            raise ValueError("PERSONAL_OPENAI_KEY not provided in environment variables")
        # check if data path is valid
        if not os.path.exists(data_folder):
            raise ValueError("Invalid DATA_FOLDER path")
        
        # initialize openai client
        self.openai_client = openai.OpenAI(api_key=os.environ.get("PERSONAL_OPENAI_KEY"))
        # initialize index service
        self.index_service = IndexingService(data_folder)
        print("RAG Solution object initialized")

    def generate_response(self, question: str) -> str:
        """
            This method will take question as input and return
            response generated from llm.

        """
        context: list[str] = self.index_service.retrive_docs(question)
        context: str = " ".join(context)

        prompt = f"Given the context: {context}, provide an answer to the question: `{question}`."
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': 'system', 'content': "You have to answer question based on context given"},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=300,
            temperature=0.5
        )
        return response.choices[0].message.content

class IndexingService:
    
    def __init__(self, data_folder: str):
        """
            init method for index service. Loads press release data.
            Initializes object of embedding service as well. And
            generates index from embeddings of data folder.

        """
        self.data_folder: str = data_folder
        self.press_release_data: list[str] = []
        self.index = None
        self.embedding_service = EmbeddingService()

        # load data into array
        self.load_press_release_data()
        # store embeddings for all data present in folder
        self.press_release_data_embeddings = np.array(
            self.embedding_service.generate_embedding_in_bulk(self.press_release_data)
        )
        # generates FAISS index
        self.generate_index()
        print("FAISS index generated")


    def generate_index(self):
        """
            This method generates index for semantic search
        """
        dimension: int = len(self.press_release_data_embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.press_release_data_embeddings)

    def load_press_release_data(self):
        """
        This method loads data from folder into an array
        """
        files: list[str] = os.listdir(self.data_folder)
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path: str = os.path.join(self.data_folder, file_name)
                text: str = open(file_path, encoding='utf-8').read().replace("\n", " ")
                self.press_release_data.append(text)

    def retrive_docs(self, question: str, top_k: int=5) -> list[str]:
        """
            This method searches for matching docs in index based on question 
            Returns:
                list of matching press release data
        """
        question_embedding: list = self.embedding_service.generate_embedding(question)
        _, indices = self.index.search(np.array([question_embedding]), top_k)
        return [self.press_release_data[idx] for idx in indices[0]]

class EmbeddingService:

    def __init__(self):
        """
        init for embedding service
        """
        self.openai_client = openai.OpenAI(api_key=os.environ.get("PERSONAL_OPENAI_KEY"))
        self.db_path = 'embeddings.db'
        self._initialize_db()

    def _initialize_db(self):
        """
        Initialize the SQLite database for storing embeddings
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                text TEXT PRIMARY KEY,
                embedding TEXT
            )
        """)
        conn.commit()
        conn.close()

    def _fetch_embedding_from_db(self, text: str):
        """
        Fetch embedding from SQLite database
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT embedding FROM embeddings WHERE text = ?", (text,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def _store_embedding_in_db(self, text: str, embedding: list):
        """
        Store embedding in SQLite database
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO embeddings (text, embedding) VALUES (?, ?)", 
                       (text, str(embedding)))
        conn.commit()
        conn.close()

    def generate_embedding_in_bulk(self, data_array: list[str]) -> list[list]:
        """
        This method takes data array as input to generate 
        embeddings in bulk using OPENAI API.
        Returns:
            List of embeddings
        """
        embedding_array: list[list] = []
        print(f"Generating embeddings for {len(data_array)} docs")
        for text in data_array:
            embedding_array.append(self.generate_embedding(text))
        return embedding_array

    def generate_embedding(self, text: str) -> list:
        """
        This method generates embeddings of text using OPENAI API
        It checks whether embedding already generated and stored. 
        Return stored embedding if exists else generates new one and stores in DB
        """
        text = text.replace('\n', " ")
        # fetch from db if exists
        existing_embedding = self._fetch_embedding_from_db(text)
        if existing_embedding:
            return eval(existing_embedding)
        # generate new embedding
        embedding = self.openai_client.embeddings.create(input = [text], model="text-embedding-3-small").data[0].embedding
        # store new embedding for future use
        self._store_embedding_in_db(text, embedding)
        return embedding

