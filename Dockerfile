# Utilizar una imagen base de Airflow
FROM apache/airflow:2.0.0-python3.8

# Copiar los archivos de script y DAG al contenedor
COPY dags/ /usr/local/airflow/dags/
COPY scripts/ /usr/local/airflow/scripts/
COPY requirements.txt /usr/local/airflow/requirements.txt

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r /usr/local/airflow/requirements.txt

# Comando por defecto para ejecutar Airflow
CMD ["airflow", "webserver"]

