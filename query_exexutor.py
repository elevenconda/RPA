# query_executor.py
import random
def query_kg(head_entity: str, relation: str, kg_name: str) -> list:
    """Mock function to simulate querying a KG."""
    # In real scenarios, this would involve SPARQL or API-based queries
    mock_answers = {
        'dbpedia': ['Hawaii', 'Honolulu'],
        'yago': ['Honolulu'],
        'freebase': ['Honolulu, Hawaii']
    }
    return mock_answers.get(kg_name, ["No answer found"])

def aggregate_answers(answer_dict: dict) -> list:
    """Collect and return unique answers from multiple KGs."""
    all_answers = set()
    for answers in answer_dict.values():
        all_answers.update(answers)
    return list(all_answers)