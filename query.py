"""query.py - Retrieval + Generation for The Unofficial Guide."""
import os
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq

DB_DIR = "chroma_store"
COLLECTION_NAME = "professor_reviews"
EMBED_MODEL = "all-MiniLM-L6-v2"
GROQ_MODEL = "llama-3.3-70b-versatile"
TOP_K = 4


def get_collection():
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL
    )
    client = chromadb.PersistentClient(path=DB_DIR)
    return client.get_collection(name=COLLECTION_NAME, embedding_function=embed_fn)


def retrieve(collection, question):
    results = collection.query(query_texts=[question], n_results=TOP_K)
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]
    return list(zip(docs, metas, dists))


def build_context(chunks):
    lines = []
    for i, (text, meta, dist) in enumerate(chunks, start=1):
        label = f"[{i}] {meta['professor']} - {meta['course']} (rated {meta['rating']})"
        lines.append(f"{label}\n{text}")
    return "\n\n".join(lines)


def generate(client, question, context):
    system_prompt = (
        "You answer questions about university professors using ONLY the "
        "student reviews provided in the context. Follow these rules:\n"
        "- Use only what is in the context. Do NOT use outside knowledge.\n"
        "- If the context does not contain the answer, say you don't have "
        "enough information in the reviews. Do not make anything up.\n"
        "- When reviews disagree, say so honestly and show both sides.\n"
        "- Cite the sources you used with their numbers, like [1] or [2]."
    )
    user_prompt = f"Context (student reviews):\n\n{context}\n\nQuestion: {question}"
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content


def main():
    if not os.environ.get("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY is not set.")
        return
    collection = get_collection()
    client = Groq()
    print("The Unofficial Guide - ask about OC professors. Type 'quit' to exit.\n")
    while True:
        question = input("Question: ").strip()
        if question.lower() in {"quit", "exit", ""}:
            break
        chunks = retrieve(collection, question)
        context = build_context(chunks)
        answer = generate(client, question, context)
        print("\nAnswer:")
        print(answer)
        print("\nRetrieved from:")
        for i, (_, meta, dist) in enumerate(chunks, start=1):
            print(f"  [{i}] {meta['professor']} - {meta['course']} "
                  f"(rated {meta['rating']}, distance {dist:.3f})")
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()