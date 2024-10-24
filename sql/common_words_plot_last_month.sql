SELECT pub_date AS date, SUM(LENGTH(headline) - LENGTH(REPLACE(headline, ' ', '')) + 1) AS word_count
FROM lastm_headline_analysis
WHERE strftime('%Y', pub_date) = :year
  AND strftime('%m', pub_date) = :month
GROUP BY pub_date
ORDER BY pub_date;