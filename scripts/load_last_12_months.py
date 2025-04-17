import datetime
from fetch_articles import fetch_and_store_articles

# Path settings
PROJECT_HOME = "/home/airflow/nyt_airflow_project"
DB_PATH = f"{PROJECT_HOME}/data/nyt_articles.db"
ENV_PATH = f"{PROJECT_HOME}/.env"
LOG_DIR = f"{PROJECT_HOME}/logs"

# Today's date
today = datetime.date.today()

# Loop through the last 12 months
for i in range(12):
    date = today - datetime.timedelta(days=30 * i)
    year = date.year
    month = date.month
    print(f"⏳ Loading {year}-{month:02d}...")
    fetch_and_store_articles(year, month, DB_PATH, ENV_PATH, LOG_DIR)

print("✅ Done loading last 12 months.")
