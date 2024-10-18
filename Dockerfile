FROM apache/airflow:2.5.0

USER root
RUN apt-get update && apt-get install -y \
RUN pip install --upgrade pip

USER airflow

RUN pip install --user pandas boto3 snowflake-connector-python

COPY ./dags /opt/airflow/dags
COPY ./airflow.cfg /opt/airflow/airflow.cfg
