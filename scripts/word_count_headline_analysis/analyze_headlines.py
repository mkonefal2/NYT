import os
import duckdb
import pandas as pd
import re
from collections import Counter
import datetime
from dateutil.relativedelta import relativedelta

class HeadlineAnalyzer:
    def __init__(self, db_path, output_dir, year, month):
        self.db_path = os.path.abspath(db_path)
        self.output_dir = output_dir
        self.year = year
        self.month = month
        self.con = duckdb.connect(database=self.db_path)
        self.stopwords = {'the', 'a', 's', 'to', 'in', 'its', 'be', 'has', 'it', 'and', 'of', 'for', 'on', 'with', 't', 'after', 'this', 'what', 'as', 'is', 'that', 'at', 'by', 'an', 'u', 'c', 'n', 'k', 'i', 'how', 'no', 'are', 'from', 'you'}
        self.stopwords.update([str(i) for i in range(10)])

    def fetch_headlines(self):
        query = f'''
            SELECT headline
            FROM articles
            WHERE EXTRACT(YEAR FROM pub_date) = {self.year} AND EXTRACT(MONTH FROM pub_date) = {self.month}
        '''
        headlines = self.con.execute(query).fetchall()
        return [str(headline[0]) for headline in headlines if headline[0] is not None]

    def tokenize_and_clean(self, headlines):
        all_words = ' '.join(headlines)
        words = re.findall(r'\b\w+\b', all_words.lower())
        return [word for word in words if word not in self.stopwords]

    def analyze(self):
        headlines = self.fetch_headlines()
        words = self.tokenize_and_clean(headlines)
        word_count = Counter(words)
        common_words = pd.DataFrame(word_count.most_common(200), columns=['word', 'count'])

        # Format the date to include only year and month
        current_date = f"{self.year}-{self.month:02d}"
        output_file = os.path.join(self.output_dir, f"common_words_{current_date}.csv")
        common_words.to_csv(output_file, index=False)

        # Create or replace table in DuckDB
        table_name = f'common_words_{current_date}'
        self.con.execute(f'DROP TABLE IF EXISTS "{table_name}"')
        self.con.execute(f'CREATE TABLE "{table_name}" (word TEXT, count INTEGER)')
        
        # Insert data into the DuckDB table
        temp_table_name = "temp_common_words"
        self.con.register(temp_table_name, common_words)
        self.con.execute(f'INSERT INTO "{table_name}" SELECT * FROM {temp_table_name}')
        self.con.unregister(temp_table_name)

        print(f"Data saved to {output_file} and table {table_name} created in DuckDB")

    def close_connection(self):
        self.con.close()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Analyze NYT headlines for common words.')
    parser.add_argument('year', type=int, help='Year of the articles to analyze')
    parser.add_argument('month', type=int, help='Month of the articles to analyze')
    parser.add_argument('--db_path', type=str, default='C:\\Projekty\\NYT\\data\\nyt_articles.db', help='Path to the DuckDB database')
    parser.add_argument('--output_dir', type=str, default='C:\\Projekty\\NYT\\data', help='Directory to save the output CSV')

    args = parser.parse_args()

    analyzer = HeadlineAnalyzer(args.db_path, args.output_dir, args.year, args.month)
    analyzer.analyze()
    analyzer.close_connection()
