from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.S3_hook import S3Hook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime
import pandas as pd
import io

def create_tables():
    # Connect to Snowflake
    hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')
    conn = hook.get_conn()
    cursor = conn.cursor()

    # Create four sample tables
    cursor.execute("""
    CREATE OR REPLACE TABLE table1 (id INT, name STRING);
    INSERT INTO table1 VALUES (1, 'Alice'), (2, 'Bob');
    """)
    
    cursor.execute("""
    CREATE OR REPLACE TABLE table2 (id INT, age INT);
    INSERT INTO table2 VALUES (1, 30), (2, 25);
    """)
    
    cursor.execute("""
    CREATE OR REPLACE TABLE table3 (id INT, country STRING);
    INSERT INTO table3 VALUES (1, 'USA'), (2, 'Canada');
    """)
    
    cursor.execute("""
    CREATE OR REPLACE TABLE table4 (id INT, occupation STRING);
    INSERT INTO table4 VALUES (1, 'Engineer'), (2, 'Designer');
    """)
    
    cursor.close()

def join_tables_and_save_csv():
    # Connect to Snowflake
    hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')
    conn = hook.get_conn()
    cursor = conn.cursor()

    # Join the tables
    query = """
    SELECT t1.id, t1.name, t2.age, t3.country, t4.occupation
    FROM table1 t1
    JOIN table2 t2 ON t1.id = t2.id
    JOIN table3 t3 ON t1.id = t3.id
    JOIN table4 t4 ON t1.id = t4.id;
    """
    cursor.execute(query)
    result = cursor.fetchall()

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(result, columns=['id', 'name', 'age', 'country', 'occupation'])
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    # Upload to S3
    s3_hook = S3Hook(aws_conn_id='aws_default')
    s3_hook.load_string(csv_buffer.getvalue(), key='output/joined_table.csv', bucket_name='my-s3-bucket', replace=True)
    
    cursor.close()

# Define DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 1),
    'retries': 1,
}

dag = DAG('create_and_join_tables', default_args=default_args, schedule_interval=None)

with dag:
    create_task = PythonOperator(
        task_id='create_tables',
        python_callable=create_tables
    )

    join_and_upload_task = PythonOperator(
        task_id='join_tables_and_save_csv',
        python_callable=join_tables_and_save_csv
    )

    create_task >> join_and_upload_task
