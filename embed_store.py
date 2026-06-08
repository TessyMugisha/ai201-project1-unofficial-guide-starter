"""
embed_store.py
Stage 2: Embedding + Vector Store for The Unofficial Guide RAG project.

Takes the 15 chunks from ingest.py, embeds them with all-MiniLM-L6-v2,
and stores them in a persistent ChromaDB collection.

Run this ONCE to build the store. After that, retrieval reads from disk,
so you don't re-embed every time.

Requires:
    pip install sentence-transformers chromadb
"""

import chromadb
from chromadb.utils import embedding_functions

from ingest import load_all  # reuse Stage 1

# Where ChromaDB saves the vector store on disk (persists between runs).
DB_DIR = "chroma_store"
COLLECTION_NAME = "professor_reviews"

# The embedding model named in planning.md.
# all-MiniLM-L6-v2: free, runs locally, 384-dim vectors, good for short text.
EMBED_MODEL = "all-MiniLM-L6-v2"


def build_store():
    # 1. Load the 15 chunks from Stage 1.
    print("Loading chunks from ingest.py...")
    chunks = load_all()
    print(f"Loaded {len(chunks)} chunks.\n")

    # 2. Set up the embedding function. Chroma uses this for BOTH
    #    storing chunks now AND embedding queries later, so the query
    #    and the stored vectors live in the same space. That consistency
    #    is what makes semantic search work.
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL
    )

    # 3. Open a persistent Chroma client (saves to DB_DIR on disk).
    client = chromadb.PersistentClient(path=DB_DIR)

    # Start fresh each time you build, so re-running doesn't duplicate chunks.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # collection didn't exist yet, that's fine

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn,
    )

    # 4. Add the chunks. Chroma needs three parallel lists:
    #    - documents: the text it will embed
    #    - metadatas: the professor/course/rating info for citations
    #    - ids: a unique id per chunk
    documents = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [c["metadata"]["chunk_id"] for c in chunks]

    print(f"Embedding and storing {len(documents)} chunks with {EMBED_MODEL}...")
    collection.add(documents=documents, metadatas=metadatas, ids=ids)

    # 5. Verify everything landed.
    count = collection.count()
    print(f"\nDone. Collection '{COLLECTION_NAME}' now holds {count} chunks.")

    # 6. Quick sanity query so you can see retrieval working end to end.
    print("\nSanity check query: 'which professor explains things clearly?'")
    results = collection.query(
        query_texts=["which professor explains things clearly?"],
        n_results=3,
    )
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print(f"  -> {meta['professor']} ({meta['course']}, rated {meta['rating']})")
        print(f"     {doc[:80]}...")


if __name__ == "__main__":
    build_store()
