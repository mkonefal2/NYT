# analyze_keywords.py

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

    stopwords = {
        'the', 'a', 's', 'to', 'in', 'its', 'be', 'his', 'her', 'has', 'it', 'and',
        'of', 'for', 'on', 'with', 't', 'after', 'this', 'what', 'as', 'is', 'that', 'at', 'by', 'an', 'u',
        'c', 'n', 'k', 'i', 'how', 'no', 'are', 'from', 'you', "word", "count", "new", "who", "may", "review", "about", "results", "will", "dies", "his",
        "can", "says", "why", "over", "up", "your", "day", "but", "more", "we", "was", "her", "one",
        "not", "he", "into", "say", "or", "their", "our", "all", "so", "some", "make", "year", "off",
        "d", "f", "l", "my", "bee", "could", "today", "like", "show", "life", "just", "best", "love",
        "home", "again", "right", "did", "o", "r", "re", "get", "old", "good", "big", "p", "take",
        "see", "now", "when", "with", "know", "this", "that", "here", "there", "how", "then", "too",
        "very", "out", "in", "if", "no", "at", "by", "from", "on", "as", "so", "it", "its", "such",
        "has", "have", "had", "be", "but", "not", "are", "is", "was", "were", "am", "an", "the", "a", "don", "she", "him"
    }
    stopwords.update([str(i) for i in range(10)])

    words = re.findall(r'\b\w+\b', ' '.join(headlines).lower())
    words = [w for w in words if w not in stopwords]
    word_count = Counter(words)
    common_words = pd.DataFrame(word_count.most_common(200), columns=['word', 'count'])

    current_date = f"{year}-{month:02d}"
    output_file = os.path.join(output_dir, f"common_words_{current_date}.csv")
    common_words['date'] = current_date
    common_words.to_csv(output_file, index=False)

    table_name = f'common_words_{current_date}'
    con.execute(f'DROP TABLE IF EXISTS \"{table_name}\"')
    con.execute(f'CREATE TABLE \"{table_name}\" (word TEXT, count INTEGER, date TEXT)')
    con.register('temp_words', common_words)
    con.execute(f'INSERT INTO \"{table_name}\" SELECT * FROM temp_words')
    con.unregister('temp_words')

    con.close()
