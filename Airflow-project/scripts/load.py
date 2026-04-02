import pandas as pd
import os
from airflow.hooks.postgres_hook import PostgresHook

DATA_DIR = "/opt/airflow/data"

def load_data():
    transformed_path = os.path.join(DATA_DIR, "transformed_data.csv")
    df = pd.read_csv(transformed_path)

    # Conexión a Postgres (usa la conn_id configurada en Airflow)
    hook = PostgresHook(postgres_conn_id="my_postgres")

    # Inserción fila por fila
    conn = hook.get_conn()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO airflow_data (id, userId, title, body, title_length, body_length, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row["id"],
                row["userId"],
                row["title"],
                row["body"],
                row["title_length"],
                row["body_length"],
                row["created_at"],
            ),
        )
    conn.commit()
    cursor.close()
    conn.close()