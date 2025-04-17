# nyt_articles_pipeline.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Ścieżki projektu
PROJECT_HOME = "/home/airflow/nyt_airflow_project"
SCRIPTS_PATH = os.path.join(PROJECT_HOME, "scripts")
sys.path.append(SCRIPTS_PATH)

# Import funkcji
from fetch_articles import fetch_and_store_articles
from transform_headlines import transform_article_headlines
from analyze_keywords import analyze_headline_keywords

# Obliczanie poprzedniego miesiąca
def get_previous_month(execution_date):
    prev = execution_date.replace(day=1) - timedelta(days=1)
    return prev.year, prev.month

# Zadanie: pobranie i zapisanie artykułów
def run_fetch_articles(**context):
    year, month = get_previous_month(context['execution_date'])
    fetch_and_store_articles(
        year=year,
        month=month,
        db_path=f"{PROJECT_HOME}/data/nyt_articles.db",
        dotenv_path=f"{PROJECT_HOME}/.env",
        log_directory=f"{PROJECT_HOME}/logs"
    )

# Zadanie: transformacja nagłówków
def run_transform_headlines(**context):
    year, month = get_previous_month(context['execution_date'])
    transform_article_headlines(
        year=year,
        month=month,
        db_path=f"{PROJECT_HOME}/data/nyt_articles.db",
        output_dir=f"{PROJECT_HOME}/data"
    )

# Zadanie: analiza słów kluczowych
def run_analyze_keywords(**context):
    year, month = get_previous_month(context['execution_date'])
    analyze_headline_keywords(
        year=year,
        month=month,
        db_path=f"{PROJECT_HOME}/data/nyt_articles.db",
        output_dir=f"{PROJECT_HOME}/data"
    )

# Definicja DAG-a
with DAG(
    dag_id="nyt_articles_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["nyt", "headlines"],
    default_args={"retries": 1, "retry_delay": timedelta(minutes=5)}
) as dag:

    fetch_articles = PythonOperator(
        task_id="fetch_articles",
        python_callable=run_fetch_articles,
        provide_context=True
    )

    transform_headlines = PythonOperator(
        task_id="transform_headlines",
        python_callable=run_transform_headlines,
        provide_context=True
    )

    analyze_keywords = PythonOperator(
        task_id="analyze_keywords",
        python_callable=run_analyze_keywords,
        provide_context=True
    )

    fetch_articles >> transform_headlines >> analyze_keywords
