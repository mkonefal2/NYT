import requests
import pandas as pd
import duckdb
import os
import logging
import datetime

# API key and URL
api_key = 'your_api_key_here'
current_date = datetime.date.today()
previous_month = current_date.replace(day=1) - datetime.timedelta(days=1)
year = previous_month.year
month = previous_month.month
url = f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={api_key}'

# Send GET request to the API
response = requests.get(url)
data = response.json()

# Extract articles from the response data
articles = data['response']['docs']

# Create a DataFrame from the articles data
df = pd.DataFrame(articles)

# Convert all columns to string type
df = df.astype(str)

# Full path to the database file
db_path = os.path.join(os.path.dirname(__file__), '../data/nyt_articles.db')
db_path = os.path.abspath(db_path)



# Setup logging with Date and Time
log_directory = os.path.join(os.path.dirname(__file__), '../logs')
os.makedirs(log_directory, exist_ok=True)  # Create log directory if it doesn't exist
log_file_path = os.path.join(log_directory, 'data_fetch.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to DuckDB
logging.info("Connecting to DuckDB...")
con = duckdb.connect(database=db_path)
logging.info("Connected to DuckDB.")

# Ensure the articles table exists
logging.info("Ensuring the articles table exists...")
con.execute('CREATE TABLE IF NOT EXISTS articles AS SELECT * FROM df WHERE FALSE')
logging.info("Articles table ensured.")

# Filter out articles that already exist in the database
logging.info("Filtering out articles that already exist in the database...")
existing_ids = con.execute('SELECT _id FROM articles').fetchdf()['_id'].tolist()
df_filtered = df[~df['_id'].isin(existing_ids)]
logging.info(f"Filtered articles. {len(df_filtered)} new articles found.")

# Insert new articles into the database
if not df_filtered.empty:
    con.execute('INSERT INTO articles SELECT * FROM df_filtered')
    logging.info(f"Added {len(df_filtered)} new articles to the DuckDB database.")
else:
    logging.info("No new articles to add.")

