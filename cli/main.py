"""
CLI interface for the local Wiki + RAG + Ollama system.

Run from repo root using:
    python -m cli.main <command>

Examples:
    python -m cli.main files
    python -m cli.main ask "How does retry with backoff work?"
    python -m cli.main search "retry backoff"
    python -m cli.main status
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ---------------------------------------------------------------------
# Repo / path utilities
# ---------------------------------------------------------------------

def repo_root() -> Path:
    """
    Resolve the repository root based on this file's location.

    Assumes:
        repo_root/
            cli/main.py
            rag/
            docs/wiki/
    """
    return Path(__file__).resolve().parents[1]


def wiki_root(subpath: str) -> Path:
    root = repo_root() / subpath
    if not root.exists():
        raise SystemExit(
            f"Wiki root not found: {root}\n"
            "Are you running inside the correct repository?"
        )
    return root


# ---------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------

def cmd_files(args: argparse.Namespace) -> None:
    """
    List all Markdown files in the wiki (filesystem-based, no LLM).
    """
    root = wiki_root(args.root)

    paths = sorted(root.rglob("*.md"))

    if not paths:
        print("No markdown files found.")
        return

    for p in paths:
        print(p.relative_to(root))


def cmd_ask(args: argparse.Namespace) -> None:
    """
    Ask a question using RAG + Ollama.
    """
    from rag.retriever import answer

    response = answer(args.question, k=args.k)
    print(response)


def cmd_search(args: argparse.Namespace) -> None:
    """
    Semantic search only (no generation).
    """
    from rag.store import VectorStore
    from rag.ollama_client import embed

    store = VectorStore()
    query_embedding = embed(args.query)

    results = store.search(query_embedding, k=args.k)

    if not results:
        print("No results.")
        return

    for score, path, content in results:
        print(f"\n[{path}]  score={score:.3f}")
        print("-" * 60)
        print(content.strip())


def cmd_status(args: argparse.Namespace) -> None:
    """
    Show basic repo / index health.
    """
    root = repo_root()
    db = root / "knowledge.db"

    print("Wiki status")
    print("-----------")
    print(f"Repo root     : {root}")
    print(f"Wiki exists   : {(root / 'docs/wiki').exists()}")
    print(f"Vector store  : {'✅ found' if db.exists() else '❌ missing'}")


def cmd_index(args: argparse.Namespace) -> None:
    """
    Re-index the wiki into the RAG store.
    """
    from rag.indexer import index_wiki

    index_wiki()
    print("✅ Wiki indexed successfully")


# ---------------------------------------------------------------------
# CLI setup
# ---------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="wiki",
        description="Local wiki CLI (Git + Markdown + RAG + Ollama)",
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # --- files ---
    p = sub.add_parser(
        "files",
        help="List all markdown files in the wiki",
    )
    p.add_argument(
        "--root",
        default="docs/wiki",
        help="Wiki root relative to repo root (default: docs/wiki)",
    )
    p.set_defaults(func=cmd_files)

    # --- ask ---
    p = sub.add_parser(
        "ask",
        help="Ask the wiki a question (RAG + LLM)",
    )
    p.add_argument("question")
    p.add_argument("-k", type=int, default=5, help="Number of chunks to retrieve")
    p.set_defaults(func=cmd_ask)

    # --- search ---
    p = sub.add_parser(
        "search",
        help="Semantic search only (no LLM)",
    )
    p.add_argument("query")
    p.add_argument("-k", type=int, default=5)
    p.set_defaults(func=cmd_search)

    # --- status ---
    p = sub.add_parser(
        "status",
        help="Show wiki and index status",
    )
    p.set_defaults(func=cmd_status)

    # --- index ---
    p = sub.add_parser(
        "index",
        help="Re-index the wiki into the RAG store",
    )
    p.set_defaults(func=cmd_index)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
