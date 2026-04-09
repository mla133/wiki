# rag/intent.py
from enum import Enum

class Intent(Enum):
    GIT = "git"
    WIKI = "wiki"
    HYBRID = "hybrid"

GIT_KEYWORDS = {
    "commit", "commits",
    "branch", "branches",
    "merge", "rebase",
    "diff", "patch",
    "log", "history",
    "checkout", "pull", "push",
    "head", "hash", "sha",
    "author", "message",
    "changed", "modified",
}

GIT_PHRASES = {
    "last commit",
    "previous commit",
    "recent commit",
    "commit message",
    "commit history",
    "what changed",
    "who changed",
    "when was",
    "diff between",
}

WIKI_CUES = {
    "explain", "what is", "how does", "why", "overview", "guide"
}

def detect_intent(text: str) -> Intent:
    t = text.lower()
    git_hits = sum(1 for k in GIT_KEYWORDS if k in t) + sum(1 for p in GIT_PHRASES if p in t)
    wiki_hits = sum(1 for w in WIKI_CUES if w in t)

    if git_hits and not wiki_hits:
        return Intent.GIT
    if git_hits and wiki_hits:
        return Intent.HYBRID
    return Intent.WIKI
