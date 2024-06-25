
    SELECT source, COUNT(*) AS article_count
    FROM articles
    GROUP BY source
    ORDER BY article_count DESC;
    