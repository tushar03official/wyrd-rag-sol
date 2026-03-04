Project: Local-First Knowledge Retrieval for Wyrd Media Labs

1. Data Ingestion: The "Notion-to-Vector" Pipeline

what I did Now .

I utilized a Markdown Export strategy. Notion pages are exported as .md files and loaded via DirectoryLoader.

Reason : Markdown is the "Goldilocks" format for RAG—it preserves semantic structure (headers, lists, bold text) without the overhead of HTML or the layout chaos of PDF.

Better Strategy
For a live company wiki, manual exports don't scale. The optimal strategy is Incremental Syncing via the official Notion API.

working : A cron job or webhook listens for last_edited_time. Only pages modified since the last sync are re-embedded.

Alternative: Notion-to-Web connectors. Tools like Airbyte or Fivetran can sync Notion directly to a vector database, though they introduce external costs and complexity.

2. Chunking Strategy:

what i did now

Recursive Character Splitting (Chunk Size: 800, Overlap: 80).

Reason : I chose this because wiki documents are hierarchical. This splitter attempts to split by double-newlines (paragraphs) first, then single newlines, then spaces. This keeps related bullet points and policy headers in the same context window.

Trade-off: Larger chunks (800) provide better context for the LLM but "dilute" the embedding vector's focus.

Alternatives & Trade-offs
Fixed-Size Chunking: Fast but dangerous. It might cut a sentence like "Do NOT share passwords" into two chunks: "[Do NOT]" and "[share passwords]," completely reversing the meaning.

Semantic Chunking: Uses an LLM to find "breakpoints" where the topic changes.

Trade-off: High computational cost for local setups; potentially overkill for structured wikis.

3. Embeddings: Local CPU Efficiency

what i did now 

all-MiniLM-L6-v2 via HuggingFace.

Reason : It is a 384-dimensional model that balances performance and size (~80MB). It runs natively on the CPU with sub-100ms latency on standard Windows hardware.

Alternatives
nomic-embed-text: Higher quality (8192 context length) and natively supported by Ollama.

Why I didn't use it: It requires the Ollama service to be constantly under load for embedding tasks; using a dedicated local HuggingFace library separates the "memory" task from the "generation" task.

OpenAI text-embedding-3-small: Industry standard.

Trade-off: Breaks the "Zero Cost" and "Local-Only" requirement.

4. The Vector Store: Local Persistence
Current Implementation
ChromaDB (Local Persistent Mode).

How: It converts embeddings into a .sqlite3 and Parquet-backed file structure on disk (.vector_db/).

Reason : Zero configuration. It’s a pure-Python implementation that requires no Docker container or background service.

Alternatives
Qdrant: Higher performance for millions of vectors and supports "Filtering" (e.g., "Search only in the HR folder").

Trade-off: Requires Docker to run locally.

FAISS: Facebook’s library for extremely fast similarity search.

Trade-off: It is an "index," not a "database." It doesn't handle metadata or persistence as easily as Chroma.

5. The RAG Chain: Local Execution
Current Implementation
Ollama (Llama 3) + LCEL Pipeline.

Workflow: User Query → Embed → Vector Search (Top 4) → Strict Prompt Template → Llama 3 Generation.

Why: Ollama provides the easiest way to serve quantized GGUF models on Windows with GPU acceleration.

Alternatives
LM Studio: Great UI, but harder to integrate into a Python script.

vLLM: The fastest inference engine for production.

Trade-off: Very difficult to set up on Windows; primarily designed for Linux servers with heavy NVIDIA GPUs.

6. Where it can  Break
Tabular Data: If a policy is in a Notion table, the current RAG flattens it. The LLM might lose the relationship between a row and its header.

Image: This system is "blind" to images. If a workflow is a screenshot, it is ignored.

Also, If a question requires looking at Page A and Page B to synthesize an answer, a basic similarity search might only find one of them.



_____________________________________________________________________________________________________________________________




                                        Answer for Second Question


For the support inbox problem: Don't build an autonomous agent. Instead, build a Semantic Suggester. When a ticket arrives, the RAG system finds the top 3 most similar resolved tickets from history and "suggests" the answer to a human agent. This keeps a human in the loop, eliminates hallucinations, and scales the team 10x without the risk of AI-gone-wrong.

