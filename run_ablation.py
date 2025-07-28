def run_ablation():
    print("Running ablation study...")
    test_data = load_test_data()
    kg_index = build_kg_index()

    settings = [
        {"name": "Full RPA", "norm": True, "sem": True, "user": True},
        {"name": "No Normalization", "norm": False, "sem": True, "user": True},
        {"name": "No Semantic Matching", "norm": True, "sem": False, "user": True},
        {"name": "No User Selection", "norm": True, "sem": True, "user": False},
    ]

    all_results = {}
    for config in settings:
        print(f"\n[Config: {config['name']}]")
        result = evaluate(test_data, kg_index,
                          use_normalization=config['norm'],
                          use_semantic_matching=config['sem'],
                          use_user_selection=config['user'])
        all_results[config['name']] = result

    with open('results/ablation_results.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)

def main():
    print("Initializing system...")
    tokenizer, model = load_llama_model()

    print("Loading test data and KG index...")
    test_data = load_test_data()
    kg_index = build_kg_index()

    print("\nRunning evaluation...")
    evaluate(test_data, kg_index)

    print("\nRunning ablation experiments...")
    run_ablation()

if __name__ == '__main__':
    main()