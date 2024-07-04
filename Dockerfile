# Usamos una imagen base oficial de Python
FROM python:3.9-slim

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos los archivos necesarios al contenedor
COPY my_script.py /app/
COPY dag.py /app/

# Instalamos las dependencias necesarias
RUN pip install --no-cache-dir \
    requests \
    pandas \
    sqlalchemy \
    psycopg2-binary \
    apache-airflow==2.3.3 \
    apache-airflow-providers-postgres

# Establecemos el comando por defecto para ejecutar el scheduler de Airflow
CMD ["airflow", "scheduler"]
