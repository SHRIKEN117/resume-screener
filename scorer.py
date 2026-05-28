from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
 
# Scoring weights (must sum to 1.0)
WEIGHTS = {
    'experience': 0.40,
    'skills':     0.35,
    'education':  0.25,
}
 
 
def similarity(vec_a: list, vec_b: list) -> float:
    """Cosine similarity between two vectors, returned as 0–100."""
    a = np.array(vec_a).reshape(1, -1)
    b = np.array(vec_b).reshape(1, -1)
    score = cosine_similarity(a, b)[0][0]
    return round(float(score) * 100, 1)
 
 
def score_candidate(jd_embedding: list, resume_embeddings: dict) -> dict:
    """Score one resume against the JD. Returns per-section + overall."""
    scores = {}
    for section, weight in WEIGHTS.items():
        scores[section] = similarity(jd_embedding, resume_embeddings[section])
 
    overall = round(
        scores['experience'] * WEIGHTS['experience'] +
        scores['skills']     * WEIGHTS['skills']     +
        scores['education']  * WEIGHTS['education'],
        1
    )
    scores['overall'] = overall
    return scores
 
 
def rank_candidates(candidates: list[dict]) -> list[dict]:
    """Sort list of scored candidates by overall score descending."""
    return sorted(candidates, key=lambda x: x['scores']['overall'], reverse=True)
