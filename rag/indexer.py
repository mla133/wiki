# rag/indexer.py
from pathlib import Path
from ollama_client import embed
from store import VectorStore

def chunk(text, size=500):
    words = text.split()
    for i in range(0, len(words), size):
        yield " ".join(words[i:i+size])

def index_wiki(root="docs/wiki"):
    store = VectorStore()
    for md in Path(root).rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for part in chunk(text):
            emb = embed(part)
            store.add(str(md), part, emb)

if __name__ == "__main__":
    index_wiki()
