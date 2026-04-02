from datetime import datetime
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 6, 1),
    'retries': 1,
}

with DAG(dag_id='example_dag', default_args=default_args, schedule_interval='@daily') as dag:
    
    start = DummyOperator(task_id='start')

    bash_task = BashOperator(
        task_id='bash_task',
        bash_command='echo "Hello, Airflow!"'
    )

    def python_task():
        print("This is a Python task.")

    python_operator = PythonOperator(
        task_id='python_task',
        python_callable=python_task,
        pool='hight_priority'
    )

    end = DummyOperator(task_id='end')

    start >> bash_task >> python_operator >> end