from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import subprocess

DBT_PROJECT_DIR = "/opt/airflow/dbt/bookshop_dbt"

DBT_PROFILE_SETUP = """
mkdir -p /tmp/.dbt

cat > /tmp/.dbt/profiles.yml <<'EOF'
bookshop_dbt:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: INFJCYQ-IY94195
      user: Djidjooh
      password: bW6VDNbUMpfLD72
      role: ACCOUNTADMIN
      database: BOOKSHOP
      warehouse: COMPUTE_WH
      schema: RAW
      threads: 4
      client_session_keep_alive: false
EOF
"""

def run_ingestion():
    subprocess.run(
        ["python", "/opt/airflow/scripts/02_ingest_postgres_to_snowflake.py"],
        check=True
    )

with DAG(
    dag_id="bookflow_pipeline",
    start_date=datetime(2026, 4, 28, 20, 50),   # heure actuelle ou proche
    schedule_interval= "*/10 * * * *",
    catchup=False,
    tags=["bookflow", "snowflake", "dbt"],
) as dag:

    ingestion = PythonOperator(
        task_id="ingestion_postgres_to_snowflake",
        python_callable=run_ingestion
    )

    stg = BashOperator(
        task_id="dbt_stagging",
        bash_command=f"""
        {DBT_PROFILE_SETUP}
        cd {DBT_PROJECT_DIR}
        dbt run --select stagging --profiles-dir /tmp/.dbt
        """
    )

    wh = BashOperator(
        task_id="dbt_warehouse",
        bash_command=f"""
        {DBT_PROFILE_SETUP}
        cd {DBT_PROJECT_DIR}
        dbt run --select warehouse --profiles-dir /tmp/.dbt
        """
    )

    marts = BashOperator(
        task_id="dbt_marts",
        bash_command=f"""
        {DBT_PROFILE_SETUP}
        cd {DBT_PROJECT_DIR}
        dbt run --select marts --profiles-dir /tmp/.dbt
        """
    )

    ingestion >> stg >> wh >> marts