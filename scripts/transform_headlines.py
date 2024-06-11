import os
import duckdb
import pandas as pd
import datetime

# Połączenie z bazą danych
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/nyt_articles.db'))
con = duckdb.connect(database=db_path)

# Pobranie danych z tabeli articles, włączając pub_date
articles_df = con.execute('SELECT _id, headline, pub_date FROM articles').df()

# Przekształcenie kolumny headline z JSON na tekst
articles_df['headline'] = articles_df['headline'].apply(lambda x: eval(x)['main'])

# Dropowanie tabeli headline_analysis, jeśli istnieje
con.execute('DROP TABLE IF EXISTS headline_analysis')


# Utworzenie nowej tabeli z przekształconymi danymi, włączając pub_date
con.execute('''
CREATE TABLE headline_analysis AS 
SELECT _id, headline, pub_date
FROM articles_df
''')



# Dodanie daty do nazwy pliku
# Uzyskanie bieżącej daty i sformatowanie jej do postaci YYYY-MM-DD
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../data/headline_analysis_{current_date}.csv'))

articles_df.to_csv(csv_path, index=False)
# Zapisanie przekształconych danych do pliku CSV
print(f"Data saved to {csv_path}")