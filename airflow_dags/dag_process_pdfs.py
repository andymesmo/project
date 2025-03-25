from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from main import main

default_args = {
    'owner': 'user',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
}

with DAG(
    'process_pdfs',
    default_args=default_args,
    schedule_interval='@daily',
) as dag:
    process_pdfs_task = PythonOperator(
        task_id='process_pdfs',
        python_callable=main,
    )