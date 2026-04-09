# rag/hybrid_tools.py
from rag.git_tools import last_commit_message
from rag.ollama_client import chat

def explain_last_commit(question: str) -> str:
    msg = last_commit_message()
    prompt = (
        "Explain the following Git commit message clearly and concisely:\n\n"
        f"{msg}\n\n"
        f"Question: {question}"
    )
    return chat(prompt)
