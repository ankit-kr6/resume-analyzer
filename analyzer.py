import pdfplumber
import json
import re
import math
from collections import Counter

# ─────────────────────────────────────────────────────────────
# CORE ML FUNCTIONS — TF-IDF + COSINE SIMILARITY
# ─────────────────────────────────────────────────────────────

def tokenize(text):
    """Tokenize and clean text into words."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\+\#]', ' ', text)
    tokens = text.split()
    # Remove very short tokens except known skills like 'r', 'c'
    tokens = [t for t in tokens if len(t) > 1 or t in ['r', 'c']]
    return tokens

def compute_tf(tokens):
    """Compute Term Frequency (TF) for a list of tokens."""
    tf = Counter(tokens)
    total = len(tokens)
    if total == 0:
        return {}
    return {word: count / total for word, count in tf.items()}

def compute_idf(documents):
    """Compute Inverse Document Frequency (IDF) across documents."""
    N = len(documents)
    idf = {}
    all_words = set(word for doc in documents for word in doc)
    for word in all_words:
        doc_count = sum(1 for doc in documents if word in doc)
        idf[word] = math.log((N + 1) / (doc_count + 1)) + 1
    return idf

def compute_tfidf_vector(tf, idf):
    """Compute TF-IDF vector from TF and IDF."""
    return {word: tf_val * idf.get(word, 1.0) for word, tf_val in tf.items()}

def cosine_similarity(vec1, vec2):
    """
    Compute Cosine Similarity between two TF-IDF vectors.
    cosine_similarity = (A · B) / (||A|| * ||B||)
    Returns a value between 0 (no similarity) and 1 (identical).
    """
    # Dot product
    common_keys = set(vec1.keys()) & set(vec2.keys())
    dot_product = sum(vec1[k] * vec2[k] for k in common_keys)

    # Magnitudes
    mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    return dot_product / (mag1 * mag2)

# ─────────────────────────────────────────────────────────────
# PDF & SKILLS DATABASE
# ─────────────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text.strip()

def load_skills_db():
    """Load the job role to skills mapping from JSON database."""
    with open("skills_db.json", "r") as f:
        return json.load(f)

# ─────────────────────────────────────────────────────────────
# SKILL EXTRACTION & GAP ANALYSIS
# ─────────────────────────────────────────────────────────────

def extract_skills_from_resume(resume_text, all_skills):
    """
    Extract skills from resume using keyword matching.
    Case-insensitive matching to avoid false negatives.
    """
    resume_lower = resume_text.lower()
    found_skills = []
    for skill in all_skills:
        # Use word boundary matching for accuracy
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, resume_lower):
            found_skills.append(skill)
    return found_skills

def get_skill_gap(resume_skills, required_skills):
    """Compare resume skills with required skills for a job role."""
    matched = [s for s in required_skills if s in resume_skills]
    missing = [s for s in required_skills if s not in resume_skills]
    return matched, missing

# ─────────────────────────────────────────────────────────────
# AI-POWERED SIMILARITY SCORING
# ─────────────────────────────────────────────────────────────

def compute_ai_match_score(resume_text, required_skills):
    """
    Compute AI-powered match score using TF-IDF and Cosine Similarity.

    Algorithm:
    1. Tokenize resume text → compute TF for resume
    2. Create skill document from required skills → compute TF
    3. Compute IDF across both documents
    4. Generate TF-IDF vectors for both
    5. Compute cosine similarity between vectors
    6. Return similarity score as percentage

    This is a real NLP/ML technique used in industry-grade
    resume screening and job matching systems.
    """
    # Tokenize resume
    resume_tokens = tokenize(resume_text)

    # Create skill document (treat all required skills as a document)
    skill_text = " ".join(required_skills)
    skill_tokens = tokenize(skill_text)

    if not resume_tokens or not skill_tokens:
        return 0.0

    # Compute TF for each document
    resume_tf = compute_tf(resume_tokens)
    skill_tf = compute_tf(skill_tokens)

    # Compute IDF across both documents
    idf = compute_idf([resume_tokens, skill_tokens])

    # Compute TF-IDF vectors
    resume_tfidf = compute_tfidf_vector(resume_tf, idf)
    skill_tfidf = compute_tfidf_vector(skill_tf, idf)

    # Compute cosine similarity
    similarity = cosine_similarity(resume_tfidf, skill_tfidf)

    # Scale to percentage
    return round(similarity * 100, 2)

def compute_weighted_match_score(matched_skills, required_skills, resume_text, required_skills_list):
    """
    Compute a weighted final score combining:
    - Keyword match score (60% weight)
    - TF-IDF cosine similarity score (40% weight)

    This hybrid approach gives more accurate results than
    either method alone.
    """
    # Keyword match score (0-100)
    if len(required_skills) == 0:
        keyword_score = 0
    else:
        keyword_score = (len(matched_skills) / len(required_skills)) * 100

    # AI similarity score (0-100)
    ai_score = compute_ai_match_score(resume_text, required_skills_list)

    # Weighted combination
    final_score = (keyword_score * 0.6) + (ai_score * 0.4)

    return {
        "keyword_score": round(keyword_score, 1),
        "ai_similarity_score": round(ai_score, 1),
        "final_score": round(final_score, 1)
    }
