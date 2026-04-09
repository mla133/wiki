# tests/test_intent.py

import pytest
from rag.intent import detect_intent, Intent

@pytest.mark.parametrize(
    "question",
    [
        "What was the last commit?",
        "Tell me about the previous commit",
        "Show commit history",
        "Who authored this change?",
        "What files changed?",
    ],
)
def test_detect_git_intent(question):
    assert detect_intent(question) == Intent.GIT


@pytest.mark.parametrize(
    "question",
    [
        "How does retry with backoff work?",
        "What is a context manager?",
        "Explain mutable default arguments",
        "Why are lambdas late-bound?",
    ],
)
def test_detect_wiki_intent(question):
    assert detect_intent(question) == Intent.WIKI


@pytest.mark.parametrize(
    "question",
    [
        "Explain the last commit",
        "Why was this commit made?",
        "Explain what changed in the previous commit",
    ],
)
def test_detect_hybrid_intent(question):
    assert detect_intent(question) == Intent.HYBRID
