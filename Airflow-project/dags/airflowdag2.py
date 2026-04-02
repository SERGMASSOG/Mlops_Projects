

import logging
import pandas as pd
from airflow.models import DAG
from airflow.utils import dates
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

default_args = {
    'owner': 'airflow_hook',
    'start_date': dates.days_ago(1),
    'pool': 'hight_priority',
}

with DAG(dag_id='example_dag_with_hook', default_args=default_args, schedule_interval='@daily') as dag:
    
    start = DummyOperator(task_id='start')

    def query_postgres():
        pg_hook = PostgresHook(postgres_conn_id='my_postgres_connection')
        result = pg_hook.get_records(sql='SELECT * FROM my_table')
        print(result)
        
    # Otra forma de obtener df
    def query_postgres_2():
        pg_hook = PostgresHook(postgres_conn_id='my_postgres_connection')
        df = pg_hook.get_pandas_df(sql='SELECT * FROM my_table')
        logging.info("DataFrame obtenido de PostgreSQL:")
        df.to_csv('/tmp/my_table_data.csv', index=False)  # Guardar el DataFrame como CSV
        logging.info("DataFrame guardado como CSV en /tmp/my_table_data.csv")
        print(df)
    
    def posgres_connection():
        pg_hook = PostgresHook(postgres_conn_id='my_postgres_connection')
        conn = pg_hook.get_conn()
        print(conn)

    postgres_task = PythonOperator(
        task_id='query_postgres',
        python_callable=query_postgres
    )

    end = DummyOperator(task_id='end')

    start >> postgres_task >> end