# utils.py
from pypdf import PdfReader
import re
import json

# simple stopwords (extend as needed)
STOPWORDS = set("""
a an the and or but if then else when from with at by on of for in to is are was were this that as it
""".split())

def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text.append(page_text)
    return "\n".join(text)

def fallback_top_words(text: str, top_n=5):
    # lowercase, remove non-alpha, split
    t = text.lower()
    t = re.sub(r'[^a-z0-9\s]', ' ', t)
    tokens = [w for w in t.split() if w and w not in STOPWORDS and len(w) > 1]
    freq = {}
    for w in tokens:
        freq[w] = freq.get(w, 0) + 1
    items = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    top = items[:top_n]
    return [{"word": w, "count": c} for w, c in top]
