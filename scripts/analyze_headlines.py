# Dodaj import modułu os
import os
import duckdb
import pandas as pd
import re
from collections import Counter
import datetime

# Pełna ścieżka do pliku bazy danych
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/nyt_articles.db'))

con = duckdb.connect(database=db_path)

# Analiza najczęściej występujących słów w nagłówkach
headlines = con.execute('SELECT headline FROM headline_analysis').fetchall()
headlines = [str(headline[0]) for headline in headlines if headline[0] is not None]

# Uzyskanie bieżącej daty i sformatowanie jej do postaci YYYY-MM-DD
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Tokenizacja i czyszczenie tekstu nagłówków
all_words = ' '.join(headlines)
words = re.findall(r'\b\w+\b', all_words.lower())

# Definiuj listę słów mało znaczących
stopwords = {'the', 'a', 's', 'to', 'in','its','be' ,'has', 'it', 'and', 'of', 'for', 'on', 'with','t' , 'after','this', 'what', 'as', 'is', 'that', 'at', 'by', 'an', 'u', 'c', 'n', 'k' ,'i' , 'how' , 'no' , 'are' , 'from', 'you'}
# Filtruj słowa, usuwając stopwords
filtered_words = [word for word in words if word not in stopwords]

word_count = Counter(filtered_words)
common_words = pd.DataFrame(word_count.most_common(200), columns=['word', 'count'])
# Zapisz DataFrame do pliku CSV
common_words.to_csv(os.path.join(os.path.dirname(__file__), f"../data/common_words_{current_date}.csv"), index=False)


# Zapisanie przekształconych danych do pliku CSV
print(f"Data saved to {os.path.join(os.path.dirname(__file__), f'../data/common_words_{current_date}.csv')}")
