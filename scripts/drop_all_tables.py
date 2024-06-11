import duckdb
import os

# Pełna ścieżka do pliku bazy danych
db_path = os.path.join(os.path.dirname(__file__), '../data/nyt_articles.db')
db_path = os.path.abspath(db_path)

con = duckdb.connect(database=db_path)

# Zdropuj tabelę articles
con.execute('DROP TABLE IF EXISTS articles')

# Zdropuj tabelę transformed_articles
con.execute('DROP TABLE IF EXISTS transformed_articles')

# Usunięcie istniejącej tabeli, jeśli istnieje
con.execute('DROP TABLE IF EXISTS headline_analysis')

print("All tables dropped successfully.")
con.close()
