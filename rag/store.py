# rag/store.py
import sqlite3
import json
import math

def cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    norm = math.sqrt(sum(x*x for x in a)) * math.sqrt(sum(y*y for y in b))
    return dot / norm if norm else 0.0

class VectorStore:
    def __init__(self, path="knowledge.db"):
        self.conn = sqlite3.connect(path)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY,
            path TEXT,
            content TEXT,
            embedding TEXT
        )
        """)

    def add(self, path, content, embedding):
        self.conn.execute(
            "INSERT INTO chunks VALUES (NULL, ?, ?, ?)",
            (path, content, json.dumps(embedding))
        )
        self.conn.commit()

    def search(self, query_embedding, k=5):
        rows = self.conn.execute(
            "SELECT path, content, embedding FROM chunks"
        ).fetchall()

        scored = []
        for path, content, emb_json in rows:
            emb = json.loads(emb_json)
            scored.append((cosine(query_embedding, emb), path, content))

        scored.sort(reverse=True)
        return scored[:k]
