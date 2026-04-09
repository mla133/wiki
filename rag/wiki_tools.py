# rag/wiki_tools.py
from rag.retriever import answer as rag_answer

def answer_from_wiki(question: str, k: int = 5) -> str:
    return rag_answer(question, k=k)
