import requests
import pandas as pd
import duckdb
import os
import logging
import datetime
import argparse
from dotenv import load_dotenv

class NYTArticleETL:
    def __init__(self, dotenv_path, db_path, log_directory, year, month):
        self.dotenv_path = dotenv_path
        self.db_path = os.path.abspath(db_path)
        self.log_directory = log_directory
        self.year = year
        self.month = month
        self.api_key = self.load_api_key()
        self.setup_logging()

    def load_api_key(self):
        load_dotenv(self.dotenv_path)
        api_key = os.getenv('NYT_API_KEY')
        if not api_key:
            raise ValueError("No API key provided. Please set the NYT_API_KEY environment variable.")
        return api_key

    def setup_logging(self):
        os.makedirs(self.log_directory, exist_ok=True)
        log_file_path = os.path.join(self.log_directory, 'data_fetch.log')
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def fetch_articles(self):
        url = f'https://api.nytimes.com/svc/archive/v1/{self.year}/{self.month}.json?api-key={self.api_key}'
        response = requests.get(url)
        data = response.json()
        articles = data['response']['docs']
        return pd.DataFrame(articles).astype(str)

    def ensure_table_exists(self, con):
        logging.info("Ensuring the articles table exists...")
        con.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                _id TEXT PRIMARY KEY,
                web_url TEXT,
                snippet TEXT,
                lead_paragraph TEXT,
                abstract TEXT,
                source TEXT,
                headline TEXT,
                pub_date TIMESTAMP,
                document_type TEXT,
                news_desk TEXT,
                section_name TEXT,
                type_of_material TEXT,
                word_count INTEGER,
                uri TEXT
            )
        ''')
        logging.info("Articles table ensured.")

    def filter_existing_articles(self, con, df):
        logging.info("Filtering out articles that already exist in the database...")
        existing_ids = con.execute('SELECT _id FROM articles').fetchdf()['_id'].tolist()
        df_filtered = df[~df['_id'].isin(existing_ids)]
        logging.info(f"Filtered articles. {len(df_filtered)} new articles found.")
        return df_filtered

    def clean_dataframe(self, df):
        df['headline'] = df['headline'].apply(lambda x: eval(x).get('main') if x else '')
        columns_to_keep = ['_id', 'web_url', 'snippet', 'lead_paragraph', 'abstract', 'source', 
                           'headline', 'pub_date', 'document_type', 'news_desk',  
                           'type_of_material', 'word_count', 'uri']
        return df[columns_to_keep]

    def insert_articles(self, con, df_filtered):
        df_filtered = self.clean_dataframe(df_filtered)
        if not df_filtered.empty:
            con.execute('INSERT INTO articles SELECT * FROM df_filtered')
            logging.info(f"Added {len(df_filtered)} new articles to the DuckDB database.")
        else:
            logging.info("No new articles to add.")

    def run(self):
        logging.info("Connecting to DuckDB...")
        con = duckdb.connect(database=self.db_path)
        logging.info("Connected to DuckDB.")

        self.ensure_table_exists(con)

        df = self.fetch_articles()
        df_filtered = self.filter_existing_articles(con, df)
        self.insert_articles(con, df_filtered)
        
        con.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ETL for NYT articles.')
    parser.add_argument('year', type=int, help='Year of the articles to fetch')
    parser.add_argument('month', type=int, help='Month of the articles to fetch')
    args = parser.parse_args()

    dotenv_path = 'C:\\Projekty\\NYT\\.env'
    db_path = 'C:\\Projekty\\NYT\\data\\nyt_articles.db'
    log_directory = 'C:\\Projekty\\NYT\\logs'

    etl = NYTArticleETL(dotenv_path, db_path, log_directory, args.year, args.month)
    etl.run()
