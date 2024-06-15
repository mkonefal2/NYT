import os
import duckdb
import pandas as pd
import re
from collections import Counter
import datetime
from dateutil.relativedelta import relativedelta

class HeadlineAnalyzer:
    def __init__(self, db_path, output_dir):
        self.db_path = os.path.abspath(db_path)
        self.output_dir = output_dir
        self.con = duckdb.connect(database=self.db_path)
        self.stopwords = {'the', 'a', 's', 'to', 'in','its','be' ,'has', 'it', 'and', 'of', 'for', 'on', 'with','t' , 'after','this', 'what', 'as', 'is', 'that', 'at', 'by', 'an', 'u', 'c', 'n', 'k' ,'i' , 'how' , 'no' , 'are' , 'from', 'you'}
        self.stopwords.update([str(i) for i in range(10)])

    def fetch_headlines(self):
        headlines = self.con.execute('SELECT headline FROM lastm_headline_analysis').fetchall()
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

        # Calculate the date for the previous month
        previous_month_date = datetime.datetime.now() - relativedelta(months=1)
        # Format the date to include only year and month
        current_date = previous_month_date.strftime("%Y-%m")
        output_file = os.path.join(self.output_dir, f"common_words_{current_date}.csv")
        common_words.to_csv(output_file, index=False)

        print(f"Data saved to {output_file}")

    def close_connection(self):
        self.con.close()

if __name__ == '__main__':
    db_path = r"C:\Projekty\NYT\data\nyt_articles.db"
    output_dir = os.path.join(os.path.dirname(__file__), '../data')

    analyzer = HeadlineAnalyzer(db_path, output_dir)
    analyzer.analyze()
    analyzer.close_connection()
