import pandas as pd
import datetime
import os
import duckdb
import argparse
from dateutil.relativedelta import relativedelta

def transform_data(year, month, db_path, output_dir):
    db_path = os.path.abspath(db_path)
    con = duckdb.connect(database=db_path)

    # Retrieve data from the articles table, including pub_date
    articles_df = con.execute('SELECT _id, headline, pub_date FROM articles').df()

    # Ensure pub_date is in datetime format
    if articles_df['pub_date'].dtype == 'object':
        def safe_convert_to_date(date_str):
            try:
                return pd.to_datetime(date_str.split('T')[0], format='%Y-%m-%d', errors='coerce')
            except ValueError:
                return pd.NaT

        articles_df['pub_date'] = articles_df['pub_date'].apply(safe_convert_to_date)
        # Optionally, filter out rows where pub_date is NaT (if any conversion failed)
        articles_df = articles_df.dropna(subset=['pub_date'])

    # Calculate the first and last day of the specified month
    first_day_specified_month = datetime.datetime(year, month, 1)
    last_day_specified_month = first_day_specified_month + relativedelta(months=1) - datetime.timedelta(days=1)

    # Filter articles_df to include only rows from the specified month
    articles_df = articles_df[(articles_df['pub_date'] >= first_day_specified_month) & (articles_df['pub_date'] <= last_day_specified_month)]

    # Continue with the rest of the script if articles_df is not empty
    if not articles_df.empty:
        # Drop the lastm_headline_analysis table if it exists
        table_name = f'headline_analysis_{year}_{month:02d}'
        con.execute(f'DROP TABLE IF EXISTS {table_name}')

        # Create an empty table with the correct structure
        con.execute(f'''
        CREATE TABLE {table_name} (
            _id VARCHAR,
            headline TEXT,
            pub_date DATE
        )
        ''')

        # Insert data from DataFrame into the newly created table
        for index, row in articles_df.iterrows():
            con.execute(f'''
            INSERT INTO {table_name} (_id, headline, pub_date) VALUES (?, ?, ?)
            ''', (row['_id'], row['headline'], row['pub_date']))

        # Construct the file path with the updated date
        current_date = f'{year}-{month:02d}'
        csv_path = os.path.abspath(os.path.join(output_dir, f'headline_analysis_{current_date}.csv'))

        # Save the transformed data to a CSV file
        articles_df.to_csv(csv_path, index=False)
        print(f"Data saved to {csv_path}")
    else:
        print(f"No data for {year}-{month:02d}.")

    # Close the connection to the database
    con.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transform NYT articles data for a specified month.')
    parser.add_argument('year', type=int, help='Year of the articles')
    parser.add_argument('month', type=int, help='Month of the articles')
    parser.add_argument('--db_path', type=str, default='C:\\Projekty\\NYT\\data\\nyt_articles.db', help='Path to the DuckDB database')
    parser.add_argument('--output_dir', type=str, default='C:\\Projekty\\NYT\\data', help='Directory to save the output CSV')

    args = parser.parse_args()
    transform_data(args.year, args.month, args.db_path, args.output_dir)
