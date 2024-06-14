import os
import duckdb
import pandas as pd
import datetime

# Connect to the database
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:\\Projekty\\NYT\\data\\nyt_articles.db'))
con = duckdb.connect(database=db_path)

# Retrieve data from the articles table, including pub_date
articles_df = con.execute('SELECT _id, headline, pub_date FROM articles').df()

# Transform the headline column from JSON to text
articles_df['headline'] = articles_df['headline'].apply(lambda x: eval(x)['main'])

# Adjust pub_date by removing the time part and converting to date format
articles_df['pub_date'] = articles_df['pub_date'].str.split('T').str[0]
articles_df['pub_date'] = pd.to_datetime(articles_df['pub_date'])

# Drop the headline_analysis table if it exists
con.execute('DROP TABLE IF EXISTS headline_analysis')

# Instead of creating a table directly from DataFrame (which is incorrect in the original script),
# we should insert the data from the DataFrame into the database.
# First, create an empty table with the correct structure.
con.execute('''
CREATE TABLE headline_analysis (
    _id VARCHAR,
    headline TEXT,
    pub_date DATE
)
''')

# Insert data from DataFrame into the newly created table
for index, row in articles_df.iterrows():
    con.execute('''
    INSERT INTO headline_analysis (_id, headline, pub_date) VALUES (?, ?, ?)
    ''', (row['_id'], row['headline'], row['pub_date']))

# Add the date to the file name
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'C:\\Projekty\\NYT\\data\\headline_analysis_{current_date}.csv'))

# Save the transformed data to a CSV file
articles_df.to_csv(csv_path, index=False)
print(f"Data saved to {csv_path}")