import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import duckdb
import os
import argparse

class WordCloudGenerator:
    def __init__(self, db_path, output_dir, year, month):
        self.year = year
        self.month = month
        self.db_path = db_path
        self.output_dir = output_dir

    def load_data(self):
        con = duckdb.connect(database=self.db_path)
        table_name = f'common_words_{self.year}-{self.month:02d}'
        query = f'''
            SELECT word, count
            FROM "{table_name}"
        '''
        df = con.execute(query).fetchdf()
        con.close()
        return df

    def generate_wordcloud(self, df):
        word_freq = {row['word']: row['count'] for index, row in df.iterrows()}
        wordcloud = WordCloud(width=1600, height=800, background_color="#232136", mode="RGBA").generate_from_frequencies(word_freq)

        plt.figure(figsize=(20, 10), dpi=100)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, f'common_words_cloud_{self.year}_{self.month}.png')
        plt.savefig(output_path, format='png', transparent=True, bbox_inches='tight', pad_inches=0)
        plt.close()
        print(f"Word cloud saved to {output_path}")

    def run(self):
        data = self.load_data()
        self.generate_wordcloud(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate word cloud for a specific month.')
    parser.add_argument('year', type=int, help='Year of the articles')
    parser.add_argument('month', type=int, help='Month of the articles')
    parser.add_argument('--db_path', type=str, default='C:\\Projekty\\NYT\\data\\nyt_articles.db', help='Path to the DuckDB database')
    parser.add_argument('--output_dir', type=str, default='C:\\Projekty\\NYT\\static\\plots', help='Directory to save the output wordcloud')

    args = parser.parse_args()
    generator = WordCloudGenerator(args.db_path, args.output_dir, args.year, args.month)
    generator.run()
