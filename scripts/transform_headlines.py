# transform_headlines.py

import pandas as pd
import datetime
import os
import duckdb
from dateutil.relativedelta import relativedelta

def transform_article_headlines(year, month, db_path, output_dir):
    con = duckdb.connect(database=os.path.abspath(db_path))
    articles_df = con.execute('SELECT _id, headline, pub_date FROM articles').df()

    if articles_df['pub_date'].dtype == 'object':
        articles_df['pub_date'] = pd.to_datetime(articles_df['pub_date'].str[:10], errors='coerce')
        articles_df = articles_df.dropna(subset=['pub_date'])

    first_day = datetime.datetime(year, month, 1)
    last_day = first_day + relativedelta(months=1) - datetime.timedelta(days=1)
    articles_df = articles_df[(articles_df['pub_date'] >= first_day) & (articles_df['pub_date'] <= last_day)]

    if not articles_df.empty:
        table_name = f'headline_analysis_{year}_{month:02d}'
        con.execute(f'DROP TABLE IF EXISTS {table_name}')
        con.execute(f'CREATE TABLE {table_name} (_id VARCHAR, headline TEXT, pub_date DATE)')

        con.register('temp_table', articles_df)
        con.execute(f'INSERT INTO {table_name} SELECT * FROM temp_table')
        con.unregister('temp_table')

        csv_path = os.path.join(output_dir, f'headline_analysis_{year}-{month:02d}.csv')
        articles_df.to_csv(csv_path, index=False)

    con.close()
