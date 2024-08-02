import os
from urllib.parse import quote_plus
from airflow.models.connection import Connection
from dotenv import load_dotenv

load_dotenv()

host = os.environ.get("TRINO_HOST")
schema = os.environ.get("TRINO_ACADEMY")
login = os.environ.get("TRINO_LOGIN")
password = os.environ.get("TRINO_PASSWORD")
port = 443

conn = Connection(
  conn_id="trino_conn",
  conn_type="trino",
  host=host,
  schema=schema,
  login=login,
  password=password,
  port=port,
  extra={
    "protocol": "https"
  },
)

env_key = f"AIRFLOW_CONN_{conn.conn_id.upper()}"
conn_uri = conn.get_uri()
print(f"{env_key}={conn_uri}")

os.environ[env_key] = conn_uri
print(conn.test_connection())  # Validate connection credentials.
