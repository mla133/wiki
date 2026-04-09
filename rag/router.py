# rag/router.py
from rag.intent import detect_intent, Intent
from rag.git_tools import last_commit_message, last_commit_summary
from rag.wiki_tools import answer_from_wiki
from rag.hybrid_tools import explain_last_commit

def answer_with_routing(question: str, k: int = 5) -> str:
    intent = detect_intent(question)

    if intent == Intent.GIT:
        # Choose specific Git answers by question
        q = question.lower()
        if "last commit" in q or "previous commit" in q:
            return last_commit_message()
        if "summary" in q:
            return last_commit_summary()
        return last_commit_message()  # safe default

    if intent == Intent.HYBRID:
        # Git facts + LLM explanation
        if "commit" in question.lower():
            return explain_last_commit(question)
        # fallback hybrid: wiki + LLM if you add more tools later
        return answer_from_wiki(question, k=k)

    # Default: WIKI
    return answer_from_wiki(question, k=k)
