# scan_links.py
import re, pathlib

for md in pathlib.Path("wiki").rglob("*.md"):
    text = md.read_text()
    links = re.findall(r'\(([^)]+\.md)\)', text)
    for link in links:
        target = (md.parent / link).resolve()
        if not target.exists():
            print(f"Broken link in {md}: {link}")
