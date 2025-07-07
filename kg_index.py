# kg_index.py
import json
from normalize import normalize_relation
from config import KG_RELATION_FILES

def build_kg_index() -> dict:
    """Build normalized index from multiple KGs."""
    index = {}
    for kg_name, file_path in KG_RELATION_FILES.items():
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_relations = json.load(f)  # expect list of strings
        index[kg_name] = {
            rel: normalize_relation(rel)
            for rel in raw_relations
        }
    return index