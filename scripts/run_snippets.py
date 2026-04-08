## wiki/scripts/run_snippets.py

"""
Run and validate Python code snippets embedded in Markdown files.

Usage:
    python scripts/run_snippets.py
    python scripts/run_snippets.py wiki/python

Rules:
- Only ```python fenced code blocks are executed
- Each snippet runs in a fresh namespace
- Snippets should be executable (no '...')
"""

from pathlib import Path
import re
import sys
import traceback

FENCE_RE = re.compile(r"```python\s+(.*?)```", re.S)

def extract_snippets(markdown_text):
    return FENCE_RE.findall(markdown_text)

def run_snippet(code, filename, index):
    namespace = {}
    try:
        exec(code, namespace, namespace)
        print(f"Snippet {index} - {filename} --> PASSED")
    except Exception as e:
        print("\nSnippet FAILED")
        print(f"File: {filename}")
        print(f"Snippet #{index}")
        print("-" * 60)
        print(code)
        print("-" * 60)
        traceback.print_exc()
        raise SystemExit(1)

def main(root="wiki"):
    root = Path(root)
    markdown_files = list(root.rglob("*.md"))

    total = 0

    for md in markdown_files:
        text = md.read_text(encoding="utf-8")
        snippets = extract_snippets(text)

        for i, snippet in enumerate(snippets, start=1):
            total += 1
            run_snippet(snippet, md, i)

    print(f"\nAll snippets passed ({total} total)")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "wiki"
    main(path)
