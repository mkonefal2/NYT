
    SELECT type_of_material, COUNT(*) AS article_count
    FROM articles
    GROUP BY type_of_material
    ORDER BY article_count DESC;
    