import requests
import pandas as pd
import duckdb
import os
import logging
from dotenv import load_dotenv

def fetch_and_store_articles(year, month, db_path, dotenv_path, log_directory):
    class NYTArticleETL:
        def __init__(self):
            self.db_path = os.path.abspath(db_path)
            self.log_directory = log_directory
            self.year = year
            self.month = month
            self.api_key = self.load_api_key()
            self.setup_logging()

        def load_api_key(self):
            load_dotenv(dotenv_path)
            api_key = os.getenv('NYT_API_KEY')
            if not api_key:
                raise ValueError("No API key provided. Please set the NYT_API_KEY environment variable.")
            return api_key

        def setup_logging(self):
            os.makedirs(self.log_directory, exist_ok=True)
            log_file_path = os.path.join(self.log_directory, 'data_fetch.log')
            logging.basicConfig(filename=log_file_path, level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s')

        def fetch_articles(self):
            url = f'https://api.nytimes.com/svc/archive/v1/{self.year}/{self.month}.json?api-key={self.api_key}'
            response = requests.get(url)

            if response.status_code != 200:
                logging.error(f"❌ Failed to fetch data from NYT API: {response.status_code} - {response.text}")
                return pd.DataFrame()

            data = response.json()
            if 'response' not in data or 'docs' not in data['response']:
                logging.warning(f"⚠️ No 'response.docs' found in NYT data for {self.year}-{self.month:02d}")
                return pd.DataFrame()

            articles = data['response']['docs']
            return pd.DataFrame(articles).astype(str)

        def new_entries_exist(self, con):
            query = f"""
                SELECT COUNT(*) FROM articles 
                WHERE strftime('%Y', pub_date) = '{self.year}' AND strftime('%m', pub_date) = '{self.month:02d}'
            """
            result = con.execute(query).fetchone()[0]
            return result == 0

        def filter_existing_articles(self, con, df):
            existing_ids = con.execute('SELECT _id FROM articles').fetchdf()['_id'].tolist()
            df_filtered = df[~df['_id'].isin(existing_ids)]
            return df_filtered

        def clean_dataframe(self, df):
            df['headline'] = df['headline'].apply(lambda x: eval(x).get('main') if x else '')

            expected_columns = [
                '_id', 'web_url', 'snippet', 'lead_paragraph', 'abstract', 'source',
                'headline', 'pub_date', 'document_type', 'news_desk', 'section_name',
                'type_of_material', 'word_count', 'uri'
            ]

            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ""

            return df[expected_columns]

        def insert_articles(self, con, df_filtered):
            df_filtered = self.clean_dataframe(df_filtered)
            if not df_filtered.empty:
                con.register('df_filtered', df_filtered)
                con.execute('INSERT INTO articles SELECT * FROM df_filtered')
                con.unregister('df_filtered')
                logging.info(f"✅ Inserted {len(df_filtered)} new articles.")
            else:
                logging.info("ℹ️ No new articles to insert.")

        def run(self):
            con = duckdb.connect(database=self.db_path)

            if not self.new_entries_exist(con):
                logging.info("🔁 Data already exists for this period. Skipping insert.")
                con.close()
                return

            df = self.fetch_articles()
            if df.empty:
                logging.warning(f"⚠️ No articles returned for {self.year}-{self.month:02d}. Skipping.")
                con.close()
                return

            df_filtered = self.filter_existing_articles(con, df)
            self.insert_articles(con, df_filtered)
            con.close()

    NYTArticleETL().run()

