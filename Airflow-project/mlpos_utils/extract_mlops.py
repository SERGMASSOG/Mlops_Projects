from sklearn.datasets import load_iris
import pandas as pd
import os

DATA_DIR = "/opt/airflow/data"

def extract_data():
    iris = load_iris(as_frame=True)
    df = iris.frame
    os.makedirs(DATA_DIR, exist_ok=True)
    raw_path = os.path.join(DATA_DIR, "iris_raw.csv")
    df.to_csv(raw_path, index=False)
    return raw_path