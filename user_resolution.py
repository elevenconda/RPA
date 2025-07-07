# user_resolution.py
def resolve_with_user_selection(answer_dict: dict):
    """Allow user to choose from conflicting KG answers."""
    print("\nMultiple answers found across KGs:")
    options = []
    for kg, answers in answer_dict.items():
        for ans in answers:
            options.append((kg, ans))
    for idx, (kg, ans) in enumerate(options):
        print(f"[{idx}] {ans} (from {kg})")

    selected = input("Select the most appropriate answer [index]: ")
    try:
        selected_idx = int(selected)
        return options[selected_idx][1]
    except (ValueError, IndexError):
        print("Invalid selection. Defaulting to first option.")
        return options[0][1]
