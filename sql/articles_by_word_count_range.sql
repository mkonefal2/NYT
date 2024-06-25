
    SELECT CASE
             WHEN word_count < 500 THEN '0-499'
             WHEN word_count BETWEEN 500 AND 999 THEN '500-999'
             WHEN word_count BETWEEN 1000 AND 1499 THEN '1000-1499'
             ELSE '1500+'
           END AS word_count_range,
           COUNT(*) AS article_count
    FROM articles
    GROUP BY word_count_range
    ORDER BY article_count DESC;
    