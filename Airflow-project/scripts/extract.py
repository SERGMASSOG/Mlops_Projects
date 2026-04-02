import requests
import pandas as pd
import os

DATA_DIR = "/opt/airflow/data"

def extract_data():
    url = "https://jsonplaceholder.typicode.com/posts"  
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data)

    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, "raw_data.csv")
    df.to_csv(file_path, index=False)
    return file_path