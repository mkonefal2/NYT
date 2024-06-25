
    SELECT news_desk, COUNT(*) AS article_count
    FROM articles
    GROUP BY news_desk
    ORDER BY article_count DESC;
    