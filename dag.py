from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import my_script

# Definir las funciones de cada tarea
def extract_data():
    url = "https://api-colombia.com/api/v1/Department"
    return my_script.extract_data_from_api(url)

def transform_data(ti):
    data = ti.xcom_pull(task_ids='extract_data')
    df = my_script.transform_data_to_dataframe(data)
    df_cleaned = my_script.clean_data(df)
    return df_cleaned

def load_data(ti):
    df_cleaned = ti.xcom_pull(task_ids='transform_data')
    engine = my_script.get_redshift_engine()
    my_script.load_data_to_redshift(df_cleaned, engine)
    my_script.verify_data_in_redshift(engine)

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

# Definir las tareas del DAG
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

# secuencia
extract_task >> transform_task >> load_task
