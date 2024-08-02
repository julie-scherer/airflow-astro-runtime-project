import os
from airflow.models.connection import Connection
from dotenv import load_dotenv

load_dotenv()

conn = Connection(
    conn_id="aws_prod_conn",
    conn_type="aws",
    login=os.environ.get("AWS_LOGIN"),  # Reference to AWS Access Key ID
    password=os.environ.get("AWS_PASSWORD"),   # Reference to AWS Secret Access Key
    # extra={
    #     # Specify extra parameters here
    #     "region_name": "us-west-2"
    # },
)

# Generate Environment Variable Name and Connection URI
env_key = f"AIRFLOW_CONN_{conn.conn_id.upper()}"
conn_uri = conn.get_uri()
print(f"{env_key}={conn_uri}")

os.environ[env_key] = conn_uri
print(conn.test_connection())  # Validate connection credentials.
