import pandas as pd
import datetime
import os
import duckdb

# Connect to the database
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:\\Projekty\\NYT\\data\\nyt_articles.db'))
con = duckdb.connect(database=db_path)

# Retrieve data from the articles table, including pub_date
articles_df = con.execute('SELECT _id, headline, pub_date FROM articles').df()



# Transform the headline column from JSON to text
articles_df['headline'] = articles_df['headline'].apply(lambda x: eval(x)['main'])

def safe_convert_to_date(date_str):
    try:
        # Attempt to split by 'T' and convert to datetime
        return pd.to_datetime(date_str.split('T')[0], format='%Y-%m-%d', errors='coerce')
    except ValueError:
        # Return NaT (Not a Time) for rows with conversion issues
        return pd.NaT

# Adjust pub_date by removing the time part and timezone before converting to date format
articles_df['pub_date'] = articles_df['pub_date'].str.split('T').str[0]
articles_df['pub_date'] = pd.to_datetime(articles_df['pub_date'], format='%Y-%m-%d')

# Optionally, filter out rows where pub_date is NaT (if any conversion failed)
articles_df = articles_df.dropna(subset=['pub_date'])

# Calculate the first and last day of the previous month
first_day_prev_month = (pd.to_datetime('now') - pd.offsets.MonthBegin(2)).normalize()
last_day_prev_month = (pd.to_datetime('now') - pd.offsets.MonthBegin(1)).normalize() - pd.Timedelta(days=1)

# Filter articles_df to include only rows from the previous month
articles_df = articles_df[(articles_df['pub_date'] >= first_day_prev_month) & (articles_df['pub_date'] <= last_day_prev_month)]


# Continue with the rest of the script if articles_df is not empty
if not articles_df.empty:
    # Drop the headline_analysis table if it exists
    con.execute('DROP TABLE IF EXISTS headline_analysis')

    # Create an empty table with the correct structure
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
else:
    print("No data for the previous month.")