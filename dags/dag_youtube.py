from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from etl_youtube import run_pipeline

default_args = {
  'owner' : 'youtube-etl',
  'retries' : 5,
  'email' : ['steveee9890@gmail.com'],
  'email_on_failure' : False,
  'email_on_retry' : False,
  'retry_delay' : timedelta(minutes=2)
}

with DAG(
  dag_id = 'youtube_etl_pipeline_v01',
  description = 'make a etl pipeline based on scrapping data from youtube',
  default_args = default_args,
  start_date = datetime(2026, 7, 4),
  schedule = '@daily'
) as dag:
  task1 = PythonOperator(
    task_id = 'complete_etl_youtube',
    python_callable = run_pipeline
  )
  
  task1