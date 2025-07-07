# config.py

# Similarity thresholds
STRING_MATCH_THRESHOLD = 0.9
EMBEDDING_MATCH_THRESHOLD = 0.8

# Embedding model for semantic similarity
SENTENCE_BERT_MODEL = 'sentence-transformers/paraphrase-MiniLM-L6-v2'

# Paths to KG relation schema files
KG_RELATION_FILES = {
    'dbpedia': 'data/relations_dbpedia.json',
    'yago': 'data/relations_yago.json',
    'freebase': 'data/relations_freebase.json'
}

# Alpha and beta for string similarity weighting
ALPHA = 0.5
BETA = 0.5
