# Utilizar una imagen base de Python ligera
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de script y DAG al contenedor
COPY my_script.py /app/
COPY dag.py /app/
COPY requirements.txt /app/

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar el scheduler de Airflow
CMD ["airflow", "scheduler"]
