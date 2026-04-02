# Pipeline ETL: API Transformación Data Warehouse
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import sys
import os

# Path de scripts
sys.path.append('scripts')

from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_data


default_args = {
    'owner': 'airflow_etl',
    'retries':1,
}

with DAG(
    'etl_pipeline',
    default_args=default_args,
    description='Pipeline ETL: API → Transformación → Data Warehouse',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:
    
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data
    )
    
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )
    
    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )
    
    extract_task >> transform_task >> load_task