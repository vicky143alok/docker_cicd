FROM apache/airflow:2.5.0

USER root
RUN apt-get update && apt-get install -y \
USER airflow
RUN pip install --upgrade pip
RUN pip install pandas boto3 snowflake-connector-python
COPY ./dags /opt/airflow/dags
COPY ./airflow.cfg /opt/airflow/airflow.cfg
