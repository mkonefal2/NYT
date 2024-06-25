import os
import argparse
import pandas as pd
import duckdb
from wordcloud import WordCloud
import plotly.express as px

class InteractiveWordCloudGenerator:
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
        data = con.execute(query).fetchdf()
        con.close()
        return data

    def generate_wordcloud(self, data):
        word_freq = dict(zip(data['word'], data['count']))
        wc = WordCloud(width=1600, height=800, background_color='#232136').generate_from_frequencies(word_freq)
        
        # Create a Plotly figure
        fig = px.imshow(wc.to_array())
        fig.update_layout(
            title={
            'text': f'Most Common Word Cloud for {self.month:02d}/{self.year}',
            'y':0.9,  # Położenie tytułu na osi Y (0.9 oznacza blisko górnej krawędzi)
            'x':0.5,  # Centrowanie tytułu
            'xanchor': 'center',  # Zakotwiczenie tytułu na środku przy zmianie wartości 'x'
            'yanchor': 'top'  # Zakotwiczenie tytułu na górze przy zmianie wartości 'y'
        },
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='#232136',
        paper_bgcolor='#232136',
        margin=dict(l=0, r=0, t=30, b=0),
        title_font=dict(  # Dodanie stylu czcionki dla tytułu
            size=16,
            color='#FFFFFF'  # Ustawienie białego koloru dla tytułu
        )
    )
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        plot_path = os.path.join(self.output_dir, f"common_words_cloud_{self.year}_{self.month:02d}.html")
        fig.write_html(plot_path)
        print(f"Word Cloud saved to {plot_path}")

    def run(self):
        data = self.load_data()
        self.generate_wordcloud(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate word cloud for a specified month.')
    parser.add_argument('year', type=int, help='Year of the data')
    parser.add_argument('month', type=int, help='Month of the data')
    parser.add_argument('--db_path', type=str, default='C:\\Projekty\\NYT\\data\\nyt_articles.db', help='Path to the DuckDB database')
    parser.add_argument('--output_dir', type=str, default=os.path.join(os.path.dirname(__file__), '../../static/plots'), help='Directory to save the output plots')

    args = parser.parse_args()
    generator = InteractiveWordCloudGenerator(args.db_path, args.output_dir, args.year, args.month)
    generator.run()
