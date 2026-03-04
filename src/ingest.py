import os
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def run_ingestion(data_path="data/", db_path=".vector_db"):
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Create it and add your .md files.")
        return

    loader = DirectoryLoader(data_path, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
    docs = loader.load()
    
    # 800/80 strategy for hierarchical wikis
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=80)
    chunks = splitter.split_documents(docs)
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_path
    )
    print(f"Success: Processed {len(chunks)} chunks into {db_path}")

if __name__ == "__main__":
    run_ingestion()