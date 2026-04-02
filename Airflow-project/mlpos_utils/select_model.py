def select_model(results):
    # Selección basada en F1
    best_model = max(results.items(), key=lambda x: x[1]["f1"])
    return best_model[0], best_model[1]