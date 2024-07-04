FROM python:3.9-slim
WORKDIR /app
COPY my_script.py /app/
COPY dag.py /app/
RUN pip install requests pandas sqlalchemy psycopg2-binary apache-airflow
CMD ["airflow", "scheduler"]
