# app/scorer.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

nlp = spacy.load('en_core_web_sm')


def get_embedding(text: str) -> np.ndarray:
    """
    Convert a block of text into a fixed-size vector (embedding).
    Think of this as the 'coordinates' of the text in meaning-space.
    Two semantically similar texts will have coordinates close to each other.
    """
    return model.encode(text, convert_to_numpy=True)


def compute_similarity(resume_text: str, jd_text: str) -> float:
    """
    Compute how semantically similar the resume and JD are.
    cosine_similarity measures the angle between two vectors — 1.0 = identical meaning,
    0.0 = completely unrelated. We return a percentage (0–100).
    """
    resume_embedding = get_embedding(resume_text).reshape(1, -1)
    jd_embedding = get_embedding(jd_text).reshape(1, -1)
    
    score = cosine_similarity(resume_embedding, jd_embedding)[0][0]
    return round(float(score) * 100, 2)  # Convert to percentage


def extract_keywords(text: str) -> set:
    """
    Extract meaningful keywords from text using spaCy.
    We keep only nouns, proper nouns, and adjectives — these carry the most
    semantic weight in resumes and job descriptions.
    We also filter out very short words (stop words like 'a', 'the', 'in').
    """
    doc = nlp(text.lower())
    keywords = set()
    
    for token in doc:
        # Keep only content words that aren't punctuation or spaces
        if token.pos_ in ('NOUN', 'PROPN', 'ADJ') and not token.is_stop and len(token.text) > 2:
            keywords.add(token.lemma_)  # lemma = root form (e.g., 'running' → 'run')
    
    return keywords


def analyze_match(resume_text: str, jd_text: str) -> dict:
    """
    The main function that ties everything together.
    Returns a structured result with score, matched keywords, and missing keywords.
    """
    similarity_score = compute_similarity(resume_text, jd_text)
    
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)
    
    # Matched = keywords that appear in both
    matched = resume_keywords.intersection(jd_keywords)
    
    # Missing = keywords the JD wants but resume doesn't mention
    missing = jd_keywords.difference(resume_keywords)
    
    # Generate a simple rating label based on score
    if similarity_score >= 75:
        rating = "Excellent Match"
    elif similarity_score >= 55:
        rating = "Good Match"
    elif similarity_score >= 35:
        rating = "Partial Match"
    else:
        rating = "Low Match — Significant gaps found"
    
    return {
        "similarity_score": similarity_score,
        "rating": rating,
        "matched_keywords": sorted(list(matched)),
        "missing_keywords": sorted(list(missing)),
        "resume_keyword_count": len(resume_keywords),
        "jd_keyword_count": len(jd_keywords),
    }