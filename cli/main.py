# cli/main.py
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ---------------------------------------------------------------------
# Repo utilities
# ---------------------------------------------------------------------

def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]

def wiki_root(subpath: str) -> Path:
    root = repo_root() / subpath
    if not root.exists():
        raise SystemExit(f"Wiki root not found: {root}")
    return root

# ---------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------

def cmd_files(args: argparse.Namespace) -> None:
    root = wiki_root(args.root)
    for p in sorted(root.rglob("*.md")):
        print(p.relative_to(root))

def cmd_ask(args: argparse.Namespace) -> None:
    from rag.router import answer_with_routing
    print(answer_with_routing(args.question, k=args.k))

def cmd_search(args: argparse.Namespace) -> None:
    from rag.store import VectorStore
    from rag.ollama_client import embed

    store = VectorStore()
    q = embed(args.query)
    for score, path, content in store.search(q, k=args.k):
        print(f"\n[{path}] score={score:.3f}\n{content}")

def cmd_status(args: argparse.Namespace) -> None:
    root = repo_root()
    db = root / "knowledge.db"
    print(f"Repo root: {root}")
    print(f"knowledge.db: {'✅' if db.exists() else '❌'}")

def cmd_index(args: argparse.Namespace) -> None:
    from rag.indexer import index_wiki_incremental
    index_wiki_incremental()
    print("✅ Index updated")

def cmd_stats(args: argparse.Namespace) -> None:
    from rag.store import VectorStore
    stats = VectorStore().stats()

    print("Wiki Index Stats")
    print("----------------")
    for k, v in stats.items():
        print(f"{k:16}: {v}")

# ---------------------------------------------------------------------
# CLI setup
# ---------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="wiki",
        description="Local Wiki CLI (Git + Markdown + RAG + Ollama)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("files")
    p.add_argument("--root", default="docs/wiki")
    p.set_defaults(func=cmd_files)

    p = sub.add_parser("ask")
    p.add_argument("question")
    p.add_argument("-k", type=int, default=5)
    p.set_defaults(func=cmd_ask)

    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("-k", type=int, default=5)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("status")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("index")
    p.set_defaults(func=cmd_index)

    p = sub.add_parser("stats")
    p.set_defaults(func=cmd_stats)

    args = parser.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main(sys.argv[1:])
