from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os
import sys

# Ścieżki do projektu
PROJECT_HOME = "/home/airflow/nyt_airflow_project"
SCRIPTS_PATH = os.path.join(PROJECT_HOME, "scripts")
sys.path.append(SCRIPTS_PATH)

from fetch_articles import fetch_and_store_articles

def load_last_12_months():
    today = datetime.today()
    db_path = os.path.join(PROJECT_HOME, "data", "nyt_articles.db")
    dotenv_path = os.path.join(PROJECT_HOME, ".env")
    log_dir = os.path.join(PROJECT_HOME, "logs")

    for i in range(12):
        date = today - relativedelta(months=i)
        year = date.year
        month = date.month
        print(f"📥 Loading {year}-{month:02d}...")
        fetch_and_store_articles(
            year=year,
            month=month,
            db_path=db_path,
            dotenv_path=dotenv_path,
            log_directory=log_dir
        )

# Definicja DAG-a
with DAG(
    dag_id="nyt_backfill_12_months",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@once",
    catchup=False,
    tags=["nyt", "backfill"],
    default_args={"owner": "airflow", "retries": 0}
) as dag:

    backfill = PythonOperator(
        task_id="load_last_12_months",
        python_callable=load_last_12_months
    )

