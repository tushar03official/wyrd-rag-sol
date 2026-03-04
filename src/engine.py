from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class WyrdAI:
    def __init__(self, db_path=".vector_db"):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectorstore = Chroma(persist_directory=db_path, embedding_function=self.embeddings)
        self.llm = OllamaLLM(model="llama3")

    def get_chain(self):
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
        
        template = """You are the Wyrd Media Labs Assistant. Use ONLY the context below to answer.
        If the answer isn't there, say 'Information not found in Wiki'. 
        
        Context: {context}
        Question: {question}
        Answer:"""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        return (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt 
            | self.llm 
            | StrOutputParser()
        )