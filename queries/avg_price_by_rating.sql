SELECT  ratings_average,  AVG(price_euros)
FROM vintages
WHERE ratings_average > 4.0
GROUP BY ratings_average
ORDER BY ratings_average ASC
LIMIT 10