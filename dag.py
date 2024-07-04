from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import my_script 

# Definir la función que ejecutará el script
def run_script():
    my_script.main()

# Definir el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'redshift_data_pipeline',
    default_args=default_args,
    description='Pipeline para cargar datos en Redshift',
    schedule_interval=timedelta(days=1),
)

run_script_task = PythonOperator(
    task_id='run_script',
    python_callable=run_script,
    dag=dag,
)
