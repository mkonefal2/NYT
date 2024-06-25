
    SELECT strftime('%Y-%m', pub_date) AS month, COUNT(*) AS article_count
    FROM articles
    GROUP BY month
    ORDER BY month;
    