
import os
import duckdb
import pandas as pd
import re
from collections import Counter


def analyze_headline_keywords(year, month, db_path, output_dir):
    con = duckdb.connect(database=os.path.abspath(db_path))

    query = f'''
        SELECT headline
        FROM articles
        WHERE EXTRACT(YEAR FROM pub_date) = {year} AND EXTRACT(MONTH FROM pub_date) = {month}
    '''
    headlines = con.execute(query).fetchall()
    headlines = [str(headline[0]) for headline in headlines if headline[0] is not None]

    stopwords = {...} 

    words = re.findall(r'\b\w+\b', ' '.join(headlines).lower())
    words = [w for w in words if w not in stopwords]
    word_count = Counter(words)
    common_words = pd.DataFrame(word_count.most_common(200), columns=['word', 'count'])

    current_date = f"{year}-{month:02d}"
    output_file = os.path.join(output_dir, f"common_words_{current_date}.csv")
    common_words.to_csv(output_file, index=False)

    table_name = f'common_words_{current_date}'
    con.execute(f'DROP TABLE IF EXISTS "{table_name}"')
    con.execute(f'CREATE TABLE "{table_name}" (word TEXT, count INTEGER, date TEXT)')
    con.register('temp_words', common_words)
    con.execute(f'INSERT INTO "{table_name}" SELECT * FROM temp_words')
    con.unregister('temp_words')
    con.close()