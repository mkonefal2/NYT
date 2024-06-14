import requests
import pandas as pd
import duckdb
import os
import logging
import datetime
from dotenv import load_dotenv
import argparse  # Import argparse module

# Setup argument parser
parser = argparse.ArgumentParser(description='Download articles from a specified month and year.')
parser.add_argument('--year', type=int, help='Year of the articles to download', default=datetime.date.today().year)
parser.add_argument('--month', type=int, help='Month of the articles to download', default=(datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).month)
args = parser.parse_args()

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('NYT_API_KEY')
if not api_key:
    raise ValueError("No API key provided. Please set the NYT_API_KEY environment variable.")

# Use arguments for year and month
year = args.year
month = args.month
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
