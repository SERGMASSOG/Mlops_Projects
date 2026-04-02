import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import joblib

DATA_DIR = "/opt/airflow/data"

def train_model():
    transformed_path = os.path.join(DATA_DIR, "iris_transformed.csv")
    df = pd.read_csv(transformed_path)

    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "logreg": LogisticRegression(max_iter=200),
        "rf": RandomForestClassifier(n_estimators=100, random_state=42)
    }

    trained_models = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        model_path = os.path.join(DATA_DIR, f"{name}_model.pkl")
        joblib.dump(model, model_path)
        trained_models[name] = model_path

    return trained_models, (X_test, y_test)