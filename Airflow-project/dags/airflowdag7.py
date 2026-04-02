# Airflow con MLOps: Un enfoque práctico para la gestión de modelos de machine learning
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys

from mlops_utils.extract_mlops import extract_data
from mlops_utils.transform_mlops import transform_data
from mlops_utils.train_mlops import train_model
from mlops_utils.evaluate import evaluate_model
from mlops_utils.select_model import select_model

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="mlops_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform_data,
    )

    train_task = PythonOperator(
        task_id="train",
        python_callable=train_model,
    )

    evaluate_task = PythonOperator(
        task_id="evaluate",
        python_callable=evaluate_model,
    )

    select_task = PythonOperator(
        task_id="select",
        python_callable=select_model,
    )

    extract_task >> transform_task >> train_task >> evaluate_task >> select_task
