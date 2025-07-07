
# normalize.py
import re
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

def normalize_relation(rel: str) -> str:
    """Standardize relation string format."""
    rel = rel.lower()
    rel = re.sub(r'[_/]', ' ', rel)  # replace underscores and slashes with spaces
    rel = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', rel)  # camelCase to space
    tokens = nltk.word_tokenize(rel)
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]
    return ' '.join(lemmatized)
