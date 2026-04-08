# rag/retriever.py
from rag.ollama_client import embed, chat
from rag.store import VectorStore

def answer(question, k=5):
    store = VectorStore()
    q_emb = embed(question)
    hits = store.search(q_emb, k=k)

    context = "\n\n".join(
        f"[{path}]\n{content}"
        for _, path, content in hits
    )

    return chat(question, context)
