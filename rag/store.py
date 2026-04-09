# rag/store.py
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Iterable
import json
import math

DB_PATH = Path("knowledge.db")


class VectorStore:
    def __init__(self, path: Path = DB_PATH):
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS index_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            git_commit TEXT NOT NULL,
            indexed_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS documents (
            doc_id INTEGER PRIMARY KEY,
            path TEXT NOT NULL UNIQUE,
            last_modified_commit TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS chunks (
            chunk_id INTEGER PRIMARY KEY,
            doc_id INTEGER NOT NULL,
            content_hash TEXT NOT NULL,
            content TEXT NOT NULL,
            embedding BLOB NOT NULL,
            git_commit TEXT NOT NULL,
            FOREIGN KEY (doc_id) REFERENCES documents(doc_id) ON DELETE CASCADE,
            UNIQUE (doc_id, content_hash)
        );
        """)

    # --- index state -------------------------------------------------

    def get_indexed_commit(self) -> str | None:
        row = self.conn.execute(
            "SELECT git_commit FROM index_state WHERE id = 1"
        ).fetchone()
        return row[0] if row else None

    def set_indexed_commit(self, commit: str) -> None:
        self.conn.execute("""
            INSERT INTO index_state (id, git_commit, indexed_at)
            VALUES (1, ?, datetime('now'))
            ON CONFLICT(id) DO UPDATE SET
                git_commit = excluded.git_commit,
                indexed_at = excluded.indexed_at
        """, (commit,))
        self.conn.commit()

    # --- document ops -----------------------------------------------

    def upsert_document(self, path: str, commit: str) -> int:
        cur = self.conn.execute("""
            INSERT INTO documents (path, last_modified_commit)
            VALUES (?, ?)
            ON CONFLICT(path) DO UPDATE SET
                last_modified_commit = excluded.last_modified_commit
        """, (path, commit))
        self.conn.commit()

        row = self.conn.execute(
            "SELECT doc_id FROM documents WHERE path = ?",
            (path,),
        ).fetchone()
        return row[0]

    def delete_document(self, path: str) -> None:
        self.conn.execute(
            "DELETE FROM documents WHERE path = ?",
            (path,),
        )
        self.conn.commit()

    # --- chunk ops ---------------------------------------------------

    def delete_chunks_for_doc(self, doc_id: int) -> None:
        self.conn.execute(
            "DELETE FROM chunks WHERE doc_id = ?",
            (doc_id,),
        )
        self.conn.commit()

    def insert_chunks(
        self,
        doc_id: int,
        commit: str,
        chunks: Iterable[tuple[str, str, list[float]]],
    ) -> None:
        """
        chunks: iterable of (content_hash, content, embedding)
        """
        self.conn.executemany("""
            INSERT OR IGNORE INTO chunks
                (doc_id, content_hash, content, embedding, git_commit)
            VALUES (?, ?, ?, ?, ?)
        """, (
            (doc_id, h, c, json.dumps(e), commit)
            for (h, c, e) in chunks
        ))
        self.conn.commit()

    # --- stats ------------------------------------------------------

    def stats(self) -> dict:
        cur = self.conn.cursor()

        index_row = cur.execute(
            "SELECT git_commit, indexed_at FROM index_state WHERE id = 1"
        ).fetchone()

        doc_count = cur.execute(
            "SELECT COUNT(*) FROM documents"
        ).fetchone()[0]

        chunk_count = cur.execute(
            "SELECT COUNT(*) FROM chunks"
        ).fetchone()[0]

        chunk_docs = cur.execute(
            "SELECT COUNT(DISTINCT doc_id) FROM chunks"
        ).fetchone()[0]

        return {
            "indexed_commit": index_row[0] if index_row else None,
            "indexed_at": index_row[1] if index_row else None,
            "documents": doc_count,
            "chunks": chunk_count,
            "docs_with_chunks": chunk_docs,
        }


    # --- vector search ---------------------------------------------

    def search(self, query_embedding: list[float], k: int = 5):
        """
        Return top-k (score, path, content) results.
        """
        cur = self.conn.cursor()

        rows = cur.execute("""
            SELECT
                d.path,
                c.content,
                c.embedding
            FROM chunks c
            JOIN documents d ON d.doc_id = c.doc_id
        """).fetchall()

        def cosine(a, b):
            dot = sum(x * y for x, y in zip(a, b))
            na = math.sqrt(sum(x * x for x in a))
            nb = math.sqrt(sum(y * y for y in b))
            return dot / (na * nb) if na and nb else 0.0

        scored = []
        for path, content, emb_json in rows:
            emb = json.loads(emb_json)
            score = cosine(query_embedding, emb)
            scored.append((score, path, content))

        scored.sort(reverse=True, key=lambda x: x[0])
        return scored[:k]
