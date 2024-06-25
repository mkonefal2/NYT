import pandas as pd
import os
import argparse
import duckdb
import plotly.express as px

class BarChartGenerator:
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

    def generate_chart(self, data):
        data = data.nlargest(10, 'count') 
        fig = px.bar(data, x='word', y='count', title=f'Most Common Words in NYT Headlines for {self.month:02d}/{self.year}', color_discrete_sequence=['#EC9B99'])
        fig.update_layout(
            plot_bgcolor='#232136',
            paper_bgcolor='#232136',
            font=dict(color='white'),
            xaxis=dict(title='Words', color='white'),
            yaxis=dict(title='Count', color='white')
        )

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        plot_path = os.path.join(self.output_dir, f"common_words_plot_{self.year}_{self.month:02d}.html")
        fig.write_html(plot_path)
        print(f"Plot saved to {plot_path}")

    def run(self):
        data = self.load_data()
        self.generate_chart(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate bar chart for a specified month.')
    parser.add_argument('year', type=int, help='Year of the data')
    parser.add_argument('month', type=int, help='Month of the data')
    parser.add_argument('--db_path', type=str, default='C:\\Projekty\\NYT\\data\\nyt_articles.db', help='Path to the DuckDB database')
    parser.add_argument('--output_dir', type=str, default=os.path.join(os.path.dirname(__file__), '../../static/plots'), help='Directory to save the output plots')

    args = parser.parse_args()
    generator = BarChartGenerator(args.db_path, args.output_dir, args.year, args.month)
    generator.run()
