from airflow import DAG
from airflow.utils import dates
from airflow.operators.bash_operator import BashOperator  
from airflow.operators.dummy_operator import DummyOperator

default_arg = {
    'owner': 'airflow',
    'start_date': dates.days_ago(1)
}

with DAG('creando_tareas_dinamicas',
         default_args=default_arg,
         schedule_interval='@daily') as dag:
    
    operators_list = []
    bases_de_datos = ['mysql', 'postgresql', 'mongodb']
    
    start = DummyOperator(task_id='start')

    for base in bases_de_datos:
        task = BashOperator(
            task_id=f'procesar_{base}',
            bash_command=f'echo "Procesando base de datos {base}"'
        )
        operators_list.append(task)
        
    end = DummyOperator(task_id='end')
    operators_list.append(end) # Añadimos la tarea de finalización a la lista de tareas dinámicas
    
for i in range(len(operators_list) - 1):
    operators_list[i] >> operators_list[i + 1]
    
