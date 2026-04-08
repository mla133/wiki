# rag/ollama_client.py
import requests

OLLAMA_URL = "http://localhost:11434"

def embed(text, model="nomic-embed-text"):
    r = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": model, "prompt": text},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["embedding"]

def chat(prompt, context="", model="llama3:latest"):
    full_prompt = f"""
You are a personal wiki assistant.
Use the provided context to answer precisely.

Context:
{context}

Question:
{prompt}
"""
    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": model,
            "prompt": full_prompt,
            "stream": False,
        },
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["response"]
