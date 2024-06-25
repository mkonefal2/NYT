SELECT pub_date AS date, SUM(LENGTH(headline) - LENGTH(REPLACE(headline, ' ', '')) + 1) AS word_count
FROM lastm_headline_analysis
WHERE pub_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL 1 month)
  AND pub_date < DATE_TRUNC('month', CURRENT_DATE)
GROUP BY pub_date
ORDER BY pub_date;