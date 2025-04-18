import datetime
from fetch_articles import fetch_and_store_articles
import os

PROJECT_HOME = "/home/airflow/nyt_airflow_project"

DB_PATH = os.path.join(PROJECT_HOME, "data", "nyt_articles.db")
ENV_PATH = os.path.join(PROJECT_HOME, ".env")
LOG_DIR = os.path.join(PROJECT_HOME, "logs")

today = datetime.date.today()

for i in range(12):
    date = today - datetime.timedelta(days=30 * i)
    year = date.year
    month = date.month
    print(f"📥 Loading {year}-{month:02d}...")
    fetch_and_store_articles(
        year=year,
        month=month,
        db_path=DB_PATH,
        dotenv_path=ENV_PATH,
        log_directory=LOG_DIR
    )

print("✅ Done loading last 12 months.")

