import pandas as pd
import os

DATA_DIR = "/opt/airflow/data"

def transform_data():
    raw_path = os.path.join(DATA_DIR, "iris_raw.csv")
    df = pd.read_csv(raw_path)

    # Crear nuevas features
    df["sepal_ratio"] = df["sepal length (cm)"] / df["sepal width (cm)"]
    df["petal_ratio"] = df["petal length (cm)"] / df["petal width (cm)"]

    transformed_path = os.path.join(DATA_DIR, "iris_transformed.csv")
    df.to_csv(transformed_path, index=False)
    return transformed_path