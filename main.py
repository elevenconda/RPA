# main.py
from normalize import normalize_relation
from kg_index import build_kg_index
from matcher import match_relation
from query_executor import query_kg, aggregate_answers
from user_resolution import resolve_with_user_selection

def main():
    question = input("Enter your question: ")
    head_entity = input("Enter head entity: ")
    raw_path = input("Enter relation path (from LLM): ")

    norm_path = normalize_relation(raw_path)
    kg_index = build_kg_index()
    kg_name, matched_relation, score = match_relation(norm_path, kg_index)

    print(f"\nMatched relation: {matched_relation} from {kg_name} (score={score:.3f})")

    answers = {}
    for kg in kg_index:
        answers[kg] = query_kg(head_entity, matched_relation, kg)

    all_answers = aggregate_answers(answers)
    if len(set(all_answers)) == 1:
        print(f"\nFinal Answer: {all_answers[0]}")
    else:
        final = resolve_with_user_selection(answers)
        print(f"\nFinal Answer: {final}")

if __name__ == '__main__':
    main()
