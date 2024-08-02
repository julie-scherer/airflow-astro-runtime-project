import logging
from airflow.decorators import dag, task
from airflow.utils.dates import datetime, timedelta
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base import BaseHook
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.trino.hooks.trino import TrinoHook

aws_conn_id = "aws_conn"
s3_bucket = Variable.get("S3_BUCKET")
        
default_args = {
  "owner": "Julie Scherer",
  "retries": 2,
  "retry_delay": timedelta(seconds=10),
  "execution_timeout": timedelta(hours=1),
}

@dag(
    "test_airflow_connections",
    start_date=datetime(2024, 4, 19),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
)
def test_airflow_connections():
    
    @task
    def test_postgres_connection():
        postgres_conn = BaseHook.get_connection("postgres_conn")
        postgres_hook = PostgresHook(postgres_conn_id=postgres_conn)

    test_query = "SELECT 1"
    test_query_result = postgres_hook.get_first(test_query)
    assert (
      test_query_result[0] == 1
    ), f"PostgreSQL connection test failed. Expected 1. Returned {test_query_result[0]}"

    pg_query = "SELECT * FROM bootcamp.course_content LIMIT 5"
    pg_query_result = postgres_hook.get_records(pg_query)
    assert (
      len(pg_query_result) == 5
    ), f"PostgreSQL connection test failed. Expected 5. Returned {len(pg_query_result)}"

    @task
    def test_aws_connection():
        aws_hook = S3Hook(aws_conn_id=aws_conn_id)
        test_bucket_result = aws_hook.get_bucket("test-bucket")
        assert test_bucket_result is not None, "AWS S3 connection test failed"

        s3_bucket_result = aws_hook.get_bucket(s3_bucket)
        assert s3_bucket_result is not None, "AWS S3 connection test failed"

    @task
    def aws_get_bucket():
        logging.info(f's3_bucket: {s3_bucket}')
        aws_hook = S3Hook(aws_conn_id=aws_conn_id)
        s3_bucket_result = aws_hook.get_bucket(s3_bucket)
        assert s3_bucket_result is not None, "AWS S3 connection test failed"

    @task
    def aws_load_file():
        logging.info(f's3_bucket: {s3_bucket}')
        aws_hook = S3Hook(aws_conn_id=aws_conn_id)

        try:
            s3_key = 'test.txt'
            test_file_path = f'include/{s3_key}'
            open(test_file_path, 'w')
            aws_hook.load_file(filename=test_file_path,
                               key=s3_key,
                               bucket_name=s3_bucket,
                               replace=True)
            print(
                f"File {test_file_path} successfully uploaded to {s3_bucket}/{s3_key}"
            )

        except Exception as e:
            raise AssertionError(f"AWS S3 connection test failed: {str(e)}")


    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end", trigger_rule="none_failed")
    
    # Task dependencies
    start >> [
        test_postgres_connection(),
        test_aws_connection(),
        aws_get_bucket(),
        aws_load_file(),
    ] >> end

# Instantiate the DAG    
test_airflow_connections()
