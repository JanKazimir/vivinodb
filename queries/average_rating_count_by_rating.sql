SELECT ratings_average, round(AVG(ratings_count)) AS average_ratings_count  , round(AVG(price_euros)) AS average_price 
FROM vintages
WHERE ratings_average > 4.0 --AND ratings_count > 100
GROUP BY ratings_average
ORDER BY ratings_average ASC