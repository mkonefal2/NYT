import os
import duckdb
import pandas as pd
import datetime

# Connect to the database
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/nyt_articles.db'))
con = duckdb.connect(database=db_path)

# Retrieve data from the articles table, including pub_date
articles_df = con.execute('SELECT _id, headline, pub_date FROM articles').df()

# Transform the headline column from JSON to text
articles_df['headline'] = articles_df['headline'].apply(lambda x: eval(x)['main'])

# Drop the headline_analysis table if it exists
con.execute('DROP TABLE IF EXISTS headline_analysis')

# Create a new table with the transformed data, including pub_date
con.execute('''
CREATE TABLE headline_analysis AS 
SELECT _id, headline, pub_date
FROM articles_df
''')

# Add the date to the file name
# Get the current date and format it as YYYY-MM-DD
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../data/headline_analysis_{current_date}.csv'))

articles_df.to_csv(csv_path, index=False)
# Save the transformed data to a CSV file
print(f"Data saved to {csv_path}")
