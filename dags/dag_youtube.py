from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
  'owner' : 'youtube-etl',
  'retries' : 5,
  'email' : ['steveee9890@gmail.com'],
  'email_on_failure' : False,
  'email_on_retry' : False,
  'retry_delay' : timedelta(minutes=2)
}

name = 'Steven Manurung'
age = '23'
job = 'Data Engineer'

def greet():
  print(f"Hello my name is {name}, i'm {age} years old and now i work as a {job} in impactful company in indonesia")

with DAG(
  dag_id = 'youtube_etl_pipeline_v01',
  description = 'make a etl pipeline based on scrapping data from youtube',
  default_args = default_args,
  start_date = datetime(2026, 7, 4),
  schedule = '@daily'
) as dag:
  task1 = PythonOperator(
    task_id = 'greet',
    python_callable = greet
  )
  
  task1