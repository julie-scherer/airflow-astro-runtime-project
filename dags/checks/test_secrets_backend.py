from airflow import DAG
from airflow.utils.dates import datetime, timedelta
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base import BaseHook
from airflow.operators.empty import EmptyOperator

default_args = {
    "owner": "Julie Scherer",
    "retries": 2,
    "retry_delay": timedelta(seconds=10),
    "execution_timeout": timedelta(hours=1),
}

with DAG(
    "test_secrets_backend",
    start_date=datetime(2024, 4, 19),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
) as dag:

    def get_conn(**kwargs):
        conn = BaseHook.get_connection(kwargs["my_conn_id"])
        print(
            f"Password: {conn.password}, Login: {conn.login}, URI: {conn.get_uri()}, Host: {conn.host}"
        )

    def get_var(**kwargs):
        print(f"{kwargs['var_name']}: {Variable.get(kwargs['var_name'])}")

    ### CONNECTIONS 
    postgres_conn = PythonOperator(
        task_id="postgres_conn",
        python_callable=get_conn,
        op_kwargs={"my_conn_id": "postgres_conn"},
    )
    trino_conn = PythonOperator(
        task_id="trino_conn",
        python_callable=get_conn,
        op_kwargs={"my_conn_id": "trino_conn"},
    )

    aws_conn = PythonOperator(
        task_id="aws_conn",
        python_callable=get_conn,
        op_kwargs={"my_conn_id": "aws_conn"},
    )

    ### VARIABLES 
    s3_bucket_var = PythonOperator(
        task_id="s3_bucket_var",
        python_callable=get_var,
        op_kwargs={"var_name": "S3_BUCKET"},
    )
    tabular_cred_var = PythonOperator(
        task_id="tabular_cred_var",
        python_callable=get_var,
        op_kwargs={"var_name": "TABULAR_CREDENTIAL"},
    )

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end", trigger_rule="none_failed")

    # Task dependencies
    (start >> [
        postgres_conn,
        trino_conn,
        aws_conn,
        s3_bucket_var,
        tabular_cred_var,
    ] >> end)
