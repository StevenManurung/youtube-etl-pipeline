FROM apache/airflow:3.2.2

COPY requirements.txt /

RUN pip install --user --upgrade pip
RUN pip install --user -r /requirements.txt