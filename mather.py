# matcher.py
import difflib
from sentence_transformers import SentenceTransformer, util
from config import ALPHA, BETA, STRING_MATCH_THRESHOLD, EMBEDDING_MATCH_THRESHOLD, SENTENCE_BERT_MODEL

model = SentenceTransformer(SENTENCE_BERT_MODEL)

def jaccard_similarity(a: str, b: str) -> float:
    a_set = set([a[i:i+2] for i in range(len(a)-1)])
    b_set = set([b[i:i+2] for i in range(len(b)-1)])
    return len(a_set & b_set) / len(a_set | b_set | {1e-5})

def levenshtein_similarity(a: str, b: str) -> float:
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    return ratio

def string_similarity(r1: str, r2: str) -> float:
    return ALPHA * jaccard_similarity(r1, r2) + BETA * levenshtein_similarity(r1, r2)

def embedding_similarity(r1: str, r2: str) -> float:
    emb1 = model.encode(r1, convert_to_tensor=True)
    emb2 = model.encode(r2, convert_to_tensor=True)
    return float(util.pytorch_cos_sim(emb1, emb2)[0][0])

def match_relation(normalized_input: str, kg_index: dict) -> tuple:
    """Match input path to best KG relation across all KGs."""
    best_match = (None, None, 0.0)  # (kg_name, relation, score)
    for kg_name, rel_map in kg_index.items():
        for original_rel, norm_rel in rel_map.items():
            sim = string_similarity(normalized_input, norm_rel)
            if sim >= STRING_MATCH_THRESHOLD and sim > best_match[2]:
                best_match = (kg_name, original_rel, sim)
    if best_match[0]:
        return best_match
    # Fallback to embedding
    for kg_name, rel_map in kg_index.items():
        for original_rel, norm_rel in rel_map.items():
            sim = embedding_similarity(normalized_input, norm_rel)
            if sim >= EMBEDDING_MATCH_THRESHOLD and sim > best_match[2]:
                best_match = (kg_name, original_rel, sim)
    return best_match