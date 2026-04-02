import pandas as pd
import os

DATA_DIR = "/opt/airflow/data"

def transform_data():
    raw_path = os.path.join(DATA_DIR, "raw_data.csv")
    df = pd.read_csv(raw_path)

    # Ejemplo de transformaciones
    df["title_length"] = df["title"].apply(len)
    df["body_length"] = df["body"].apply(len)
    df["created_at"] = pd.Timestamp.now()

    transformed_path = os.path.join(DATA_DIR, "transformed_data.csv")
    df.to_csv(transformed_path, index=False)
    return transformed_path
