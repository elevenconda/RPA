# experiments/run_experiments.py

import json
import random
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from matcher import match_relation
from kg_index import build_kg_index
from normalize import normalize_relation
from query_executor import query_kg, aggregate_answers
from user_resolution import resolve_with_user_selection

# Load LLaMA2-Chat-7B model (HF Transformers, assuming quantized or fine-tuned version)
def load_llama_model():
    print("Loading LLaMA2-Chat-7B model...")
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Llama-2-7b-chat-hf",
        torch_dtype=torch.float16,
        device_map="auto"
    )
    return tokenizer, model

# Load test questions (mock dataset)
def load_test_data(file_path='data/test_questions.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def evaluate(test_data, kg_index):
    hit1_count = 0
    total = len(test_data)
    all_results = []

    for i, sample in enumerate(test_data):
        question = sample['question']
        head_entity = sample['head_entity']
        raw_path = sample['relation']
        gold_answers = set(sample['answers'])

        norm_path = normalize_relation(raw_path)
        kg_name, matched_relation, score = match_relation(norm_path, kg_index)

        answers = {}
        for kg in kg_index:
            answers[kg] = query_kg(head_entity, matched_relation, kg)

        all_answers = aggregate_answers(answers)
        user_answer = resolve_with_user_selection(answers)

        hit = user_answer in gold_answers
        if hit:
            hit1_count += 1

        all_results.append({
            'question': question,
            'predicted_answer': user_answer,
            'gold_answers': list(gold_answers),
            'hit@1': hit
        })

    accuracy = hit1_count / total
    print(f"\n[Evaluation Summary] Total: {total}, Hits@1: {hit1_count}, Accuracy: {accuracy:.4f}")
    return all_results

def main():
    print("Initializing system...")
    tokenizer, model = load_llama_model()

    print("Loading test data and KG index...")
    test_data = load_test_data()
    kg_index = build_kg_index()

    print("\nRunning evaluation...")
    results = evaluate(test_data, kg_index)

    with open('results/eval_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    main()
