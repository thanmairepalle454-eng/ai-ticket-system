"""
Lightweight RAG service using pure Python.
No heavy ML dependencies - uses TF-IDF keyword matching.
Works with Python 3.15+
"""
import os
import json
import math
import re
from collections import Counter

UPLOAD_FOLDER = "uploads"
INDEX_FILE = "knowledge_index.json"


def tokenize(text):
    """Simple tokenizer: lowercase, remove punctuation, split words."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return [w for w in text.split() if len(w) > 2]


def extract_text_from_pdf(filepath):
    """Extract text from PDF using pypdf if available, else read as bytes fallback."""
    try:
        import pypdf
        reader = pypdf.PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except ImportError:
        # Fallback: try to extract readable text from PDF bytes
        with open(filepath, 'rb') as f:
            content = f.read()
        # Extract readable ASCII strings from PDF
        text = re.findall(rb'[A-Za-z0-9 .,\-:;\n\r!?\'\"()]{4,}', content)
        return ' '.join(t.decode('ascii', errors='ignore') for t in text)


def compute_tfidf(docs):
    """Compute TF-IDF scores for a list of documents."""
    N = len(docs)
    tokenized = [tokenize(doc['content']) for doc in docs]

    # Document frequency
    df = Counter()
    for tokens in tokenized:
        for word in set(tokens):
            df[word] += 1

    # TF-IDF vectors
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
    """Cosine similarity between two TF-IDF vectors."""
    common = set(vec1.keys()) & set(vec2.keys())
    if not common:
        return 0.0
    dot = sum(vec1[w] * vec2[w] for w in common)
    mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def build_index():
    """Read all PDFs, extract text, build and save search index."""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    docs = []

    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.lower().endswith('.pdf'):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            text = extract_text_from_pdf(filepath)
            if text.strip():
                docs.append({
                    "filename": filename,
                    "content": text.strip()
                })
                print(f"Indexed: {filename} ({len(text)} chars)")

    if not docs:
        print("No PDFs found in uploads folder.")
        return False

    # Save index
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

    print(f"Index built with {len(docs)} document(s).")
    return True


def query_rag(question):
    """Search the knowledge base for the best matching solution."""
    if not os.path.exists(INDEX_FILE):
        return "No knowledge base found. Please upload PDF documents first using the Upload tab."

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        docs = json.load(f)

    if not docs:
        return "Knowledge base is empty. Please upload PDF documents first."

    # Build TF-IDF vectors
    vectors = compute_tfidf(docs)

    # Query vector
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

    # Score each document
    scores = [(cosine_similarity(query_vec, vec), i) for i, vec in enumerate(vectors)]
    scores.sort(reverse=True)

    best_score, best_idx = scores[0]

    if best_score < 0.01:
        return (
            "No relevant solution found in the knowledge base.\n\n"
            "Tip: Make sure you have uploaded PDF documents with relevant IT solutions."
        )

    best_doc = docs[best_idx]
    content  = best_doc['content']

    # Strip internal "Keywords:" lines and "Source:" prefix — show clean steps only
    clean_lines = []
    for line in content.splitlines():
        stripped = line.strip()
        # Skip keyword hint lines and blank leading lines
        if stripped.lower().startswith("keywords:"):
            continue
        clean_lines.append(line)

    # Remove leading blank lines
    while clean_lines and not clean_lines[0].strip():
        clean_lines.pop(0)

    clean_content = "\n".join(clean_lines).strip()[:1500]
    return clean_content
