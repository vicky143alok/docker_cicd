FROM apache/airflow:2.5.0

USER root
RUN pip install pandas boto3 snowflake-connector-python

USER airflow
COPY ./dags /opt/airflow/dags
COPY ./airflow.cfg /opt/airflow/airflow.cfg
