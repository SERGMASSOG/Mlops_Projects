import joblib
from sklearn.metrics import accuracy_score, f1_score

def evaluate_model(trained_models, test_data):
    X_test, y_test = test_data
    results = {}

    for name, path in trained_models.items():
        model = joblib.load(path)
        y_pred = model.predict(X_test)
        results[name] = {
            "accuracy": accuracy_score(y_test, y_pred),
            "f1": f1_score(y_test, y_pred, average="macro")
        }

    return results