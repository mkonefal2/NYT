import duckdb
import os

# Full path to the database file
db_path = os.path.join(os.path.dirname(__file__), 'C:\\Projekty\\NYT\\data\\nyt_articles.db')
db_path = os.path.abspath(db_path)

con = duckdb.connect(database=db_path)

# Drop the 'articles' table
con.execute('DROP TABLE IF EXISTS articles')

# Drop the 'transformed_articles' table
con.execute('DROP TABLE IF EXISTS transformed_articles')

# Drop the 'headline_analysis' table if it exists
con.execute('DROP TABLE IF EXISTS headline_analysis')

print("All tables dropped successfully.")
con.close()
