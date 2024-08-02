import os
from airflow.models.connection import Connection
from dotenv import load_dotenv

load_dotenv()

conn = Connection(
    conn_id="postgres_conn",
    conn_type="postgres",
    host=os.environ.get("PG_HOST"),
    schema=os.environ.get("PG_DATABASE"),
    login=os.environ.get("PG_LOGIN"),
    password=os.environ.get("PG_PASSWORD"),
    port=5432,
)

# Generate Environment Variable Name and Connection URI
env_key = f"AIRFLOW_CONN_{conn.conn_id.upper()}"
conn_uri = conn.get_uri()
print(f"{env_key}={conn_uri}")

os.environ[env_key] = conn_uri
print(conn.test_connection())  # Validate connection credentials.
