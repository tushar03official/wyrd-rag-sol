Wyrd RAG: Technical Decision Log
1. Chunking Logic (Recursive 800/80)
I chose RecursiveCharacterTextSplitter with an 800-token window. Unlike a simple character split, this method respects the structural hierarchy of Markdown (Paragraphs > Sentences > Words).

Why 800? Company wikis contain dense policy blocks. 800 tokens ensure a full policy section stays within a single context window.

Why 80 overlap? To maintain "semantic continuity." If a definition is split across chunks, the 10% overlap ensures the second chunk retains the subject of the first.

2. The Local-First Stack
Model: Llama 3 (via Ollama). Native Windows support and superior reasoning compared to Mistral for internal wiki tasks.

Embeddings: all-MiniLM-L6-v2. At only 80MB, it runs purely on the CPU with zero noticeable latency, fulfilling the "no cost" requirement perfectly.

Vector Store: ChromaDB. Chosen for its "zero-config" nature. For a wiki-scale project, a full managed DB is overhead.

3. System Fragility (Where it breaks)
Table Data: Basic text RAG flattens tables. If the Wiki has a complex holiday calendar in a table, the system may struggle to map specific dates to the correct column headers.

Image Content: The current system is "blind" to diagrams. If a workflow is only shown in a .png in Notion, this system cannot "see" it.

4. The "Don't Build" Solution (Support Inbox)
To solve the support inbox problem without over-engineering: Implement a Semantic FAQ Cache.
Instead of generating a new AI response for every email, we should embed the incoming question and check for >90% similarity against a "Verified Answer Database." If a match exists, send the pre-approved answer. This is faster, safer, and 100% deterministic.