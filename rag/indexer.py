# rag/indexer.py
from __future__ import annotations

import subprocess
import hashlib
from pathlib import Path
from typing import Iterable

from rag.store import VectorStore
from rag.ollama_client import embed


WIKI_ROOT = Path("docs/wiki")
CHUNK_SIZE = 400  # words


# ------------------------------------------------------------------
# Git helpers
# ------------------------------------------------------------------

def git(cmd: list[str]) -> str:
    return subprocess.check_output(
        ["git"] + cmd,
        text=True,
    ).strip()


def current_commit() -> str:
    return git(["rev-parse", "HEAD"])


def changed_files(since: str) -> list[tuple[str, str]]:
    """
    Returns list of (status, path)
    status: A, M, D
    """
    out = git([
        "diff",
        "--name-status",
        since,
        "HEAD",
        "--",
        str(WIKI_ROOT),
    ])
    if not out:
        return []

    result = []
    for line in out.splitlines():
        status, path = line.split(maxsplit=1)
        result.append((status, path))
    return result


# ------------------------------------------------------------------
# Chunking / hashing
# ------------------------------------------------------------------

def chunk_text(text: str, size: int = CHUNK_SIZE) -> Iterable[str]:
    words = text.split()
    for i in range(0, len(words), size):
        yield " ".join(words[i:i + size])


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ------------------------------------------------------------------
# Indexing logic
# ------------------------------------------------------------------

def index_file(store: VectorStore, path: Path, commit: str) -> None:
    rel_path = str(path)
    print(f"Indexing: {path}")
    text = path.read_text(encoding="utf-8")

    doc_id = store.upsert_document(rel_path, commit)
    store.delete_chunks_for_doc(doc_id)

    chunks = []
    for chunk in chunk_text(text):
        h = content_hash(chunk)
        e = embed(chunk)
        chunks.append((h, chunk, e))

    store.insert_chunks(doc_id, commit, chunks)


def index_wiki_incremental() -> None:
    store = VectorStore()
    head = current_commit()
    last = store.get_indexed_commit()

    if last is None:
        # First index: treat everything as added
        files = [( "A", str(p) ) for p in WIKI_ROOT.rglob("*.md")]
    else:
        files = changed_files(last)

    for status, path_str in files:
        path = Path(path_str)

        if status in ("A", "M"):
            if path.exists():
                index_file(store, path, head)

        elif status == "D":
            store.delete_document(path_str)

    store.set_indexed_commit(head)
