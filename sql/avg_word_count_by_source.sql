
    SELECT source, AVG(word_count) AS avg_word_count
    FROM articles
    GROUP BY source
    ORDER BY avg_word_count DESC;
    