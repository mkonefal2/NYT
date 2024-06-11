import os
import duckdb
import pandas as pd
import re
from collections import Counter
import datetime
# Full path to the database file
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/nyt_articles.db'))

con = duckdb.connect(database=db_path)

# Analyzing the most frequently occurring words in the headlines
headlines = con.execute('SELECT headline FROM headline_analysis').fetchall()
headlines = [str(headline[0]) for headline in headlines if headline[0] is not None]

# Getting the current date and formatting it as YYYY-MM-DD
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Tokenizing and cleaning the headline text
all_words = ' '.join(headlines)
words = re.findall(r'\b\w+\b', all_words.lower())

# Define a list of stopwords
stopwords = {'the', 'a', 's', 'to', 'in','its','be' ,'has', 'it', 'and', 'of', 'for', 'on', 'with','t' , 'after','this', 'what', 'as', 'is', 'that', 'at', 'by', 'an', 'u', 'c', 'n', 'k' ,'i' , 'how' , 'no' , 'are' , 'from', 'you'}
# Filter out stopwords from the words
filtered_words = [word for word in words if word not in stopwords]

word_count = Counter(filtered_words)
common_words = pd.DataFrame(word_count.most_common(200), columns=['word', 'count'])
# Save the DataFrame to a CSV file
common_words.to_csv(os.path.join(os.path.dirname(__file__), f"../data/common_words_{current_date}.csv"), index=False)


# Save the transformed data to a CSV file
print(f"Data saved to {os.path.join(os.path.dirname(__file__), f'../data/common_words_{current_date}.csv')}")
