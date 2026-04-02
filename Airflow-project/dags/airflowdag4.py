# Ejemplo de uso para subdags en Airflow. Este ejemplo muestra cómo crear un DAG principal que contiene un SubDagOperator, el cual a su vez contiene varias tareas. El SubDagOperator permite organizar y estructurar mejor los DAGs complejos al dividirlos en sub-DAGs más pequeños y manejables.
from airflow import DAG
from airflow.utils import dates
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'start_date': dates.days_ago(1)
}

PARENT_DAG_NAME = 'my_dag'

def load_subdag(parent_dag_name, child_task_id, args):
    dag_id = f"{parent_dag_name}.{child_task_id}"
    subdag = DAG(dag_id, default_args=args, schedule_interval='@daily')

    with subdag:
        start = DummyOperator(task_id='start')
        task_1 = DummyOperator(task_id='task_1')
        task_2 = DummyOperator(task_id='task_2')
        end = DummyOperator(task_id='end')
        start >> task_1 >> task_2 >> end

    return subdag

with DAG(
    PARENT_DAG_NAME,
    default_args=default_args,
    schedule_interval='@daily'
) as dag:

    start = DummyOperator(task_id='start')

    subdag_1 = SubDagOperator(
        task_id='subdag_operator',
        subdag=load_subdag(PARENT_DAG_NAME, "subdag_operator", dag.default_args),
    )

    end = DummyOperator(task_id='end')

    start >> subdag_1 >> end