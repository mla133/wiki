# tests/test_routing.py
from rag.router import answer_with_routing
from rag.intent import Intent
import rag.router as router


def test_git_question_routes_to_git(monkeypatch):
    called = {}

    def fake_last_commit():
        called["git"] = True
        return "COMMIT MESSAGE"

    monkeypatch.setattr(
        router,
        "last_commit_message",
        fake_last_commit,
    )

    result = answer_with_routing("What was the last commit?")
    assert result == "COMMIT MESSAGE"
    assert called.get("git") is True


def test_wiki_question_routes_to_rag(monkeypatch):
    called = {}

    def fake_wiki_answer(question, k=5):
        called["wiki"] = True
        return "WIKI ANSWER"

    monkeypatch.setattr(
        router,
        "answer_from_wiki",
        fake_wiki_answer,
    )

    result = answer_with_routing("How does retry with backoff work?")
    assert result == "WIKI ANSWER"
    assert called.get("wiki") is True


def test_hybrid_question_routes_to_git_and_llm(monkeypatch):
    calls = {"git": False, "llm": False}

    def fake_explain_last_commit(question):
        calls["git"] = True
        calls["llm"] = True
        return "HYBRID ANSWER"

    monkeypatch.setattr(
        router,
        "explain_last_commit",
        fake_explain_last_commit,
    )

    result = answer_with_routing("Explain the last commit")
    assert result == "HYBRID ANSWER"
    assert calls["git"] is True
    assert calls["llm"] is True
