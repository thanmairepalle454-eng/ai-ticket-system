"""
Lightweight RAG service using pure Python.
TF-IDF keyword matching + priority prediction.
"""
import os
import json
import math
import re
from collections import Counter

UPLOAD_FOLDER = "uploads"
INDEX_FILE    = "knowledge_index.json"

# ── Priority prediction keyword map ──────────────────────────────────────────
HIGH_KEYWORDS = [
    "not working", "down", "crash", "crashed", "error", "failed", "failure",
    "urgent", "critical", "emergency", "cannot login", "locked", "blocked",
    "virus", "hack", "breach", "data loss", "deleted", "corrupted", "broken",
    "server", "network down", "no internet", "system down", "blue screen", "bsod"
]
MEDIUM_KEYWORDS = [
    "slow", "lag", "freeze", "freezing", "not syncing", "not connecting",
    "vpn", "printer", "wifi", "password", "reset", "install", "update",
    "outlook", "email", "software", "access denied", "permission"
]

def predict_priority(issue_text):
    """Predict ticket priority: High / Medium / Low based on keywords."""
    text = issue_text.lower()
    for kw in HIGH_KEYWORDS:
        if kw in text:
            return "High"
    for kw in MEDIUM_KEYWORDS:
        if kw in text:
            return "Medium"
    return "Low"


def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return [w for w in text.split() if len(w) > 2]


def extract_text_from_pdf(filepath):
    try:
        import pypdf
        reader = pypdf.PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except ImportError:
        with open(filepath, 'rb') as f:
            content = f.read()
        text = re.findall(rb'[A-Za-z0-9 .,\-:;\n\r!?\'\"()]{4,}', content)
        return ' '.join(t.decode('ascii', errors='ignore') for t in text)


def compute_tfidf(docs):
    N = len(docs)
    tokenized = [tokenize(doc['content']) for doc in docs]
    df = Counter()
    for tokens in tokenized:
        for word in set(tokens):
            df[word] += 1
    vectors = []
    for tokens in tokenized:
        tf = Counter(tokens)
        total = len(tokens) or 1
        vec = {}
        for word, count in tf.items():
            idf = math.log((N + 1) / (df[word] + 1)) + 1
            vec[word] = (count / total) * idf
        vectors.append(vec)
    return vectors


def cosine_similarity(vec1, vec2):
    common = set(vec1.keys()) & set(vec2.keys())
    if not common:
        return 0.0
    dot  = sum(vec1[w] * vec2[w] for w in common)
    mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def build_index():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    docs = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.lower().endswith('.pdf'):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            text = extract_text_from_pdf(filepath)
            if text.strip():
                docs.append({"filename": filename, "content": text.strip()})
                print(f"Indexed: {filename} ({len(text)} chars)")
    if not docs:
        print("No PDFs found in uploads folder.")
        return False
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    print(f"Index built with {len(docs)} document(s).")
    return True


def query_rag(question):
    if not os.path.exists(INDEX_FILE):
        return "No knowledge base found. Please upload PDFs from the Admin portal."
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        docs = json.load(f)
    if not docs:
        return "Knowledge base is empty. Please upload PDFs from the Admin portal."

    vectors = compute_tfidf(docs)
    query_tokens = tokenize(question)
    N = len(docs)
    df = Counter()
    for vec in vectors:
        for word in vec:
            df[word] += 1
    query_tf = Counter(query_tokens)
    total = len(query_tokens) or 1
    query_vec = {}
    for word, count in query_tf.items():
        idf = math.log((N + 1) / (df.get(word, 0) + 1)) + 1
        query_vec[word] = (count / total) * idf

    scores = [(cosine_similarity(query_vec, vec), i) for i, vec in enumerate(vectors)]
    scores.sort(reverse=True)
    best_score, best_idx = scores[0]

    if best_score < 0.01:
        return "No relevant solution found. Please contact IT support directly."

    content = docs[best_idx]['content']
    clean_lines = [l for l in content.splitlines()
                   if not l.strip().lower().startswith("keywords:")]
    while clean_lines and not clean_lines[0].strip():
        clean_lines.pop(0)
    return "\n".join(clean_lines).strip()[:1500]
