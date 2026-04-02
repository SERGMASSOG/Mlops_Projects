from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator


def create__dag(dag_id, schedule, default_args, modelo):
    dag = DAG(dag_id, schedule_interval=schedule, default_args=default_args)
    
    with dag:
        start = DummyOperator(task_id='start')
        task_1_model = BashOperator(task_id=f'task_1_{modelo}', bash_command='echo "Mostrando modelo: {{ params.modelo }}"', params={'modelo': modelo})
        
        start >> task_1_model 
        
    return dag

modelos = ['regression', 'boosting', 'svm', 'knn', 'random_forest']
for model in modelos:
    default_dag_id = {
        'owner': f'airflow_{model}',
        'start_date': days_ago(1)
    }
    
    globals()[f'modelo_{model}_dag'] = create__dag(f'modelo_{model}_dag', '@daily', default_dag_id, model)

