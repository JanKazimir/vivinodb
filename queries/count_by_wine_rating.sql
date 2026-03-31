SELECT ratings_average, COUNT(distinct(id)) AS count
FROM wines
GROUP BY ratings_average
ORDER BY ratings_average DESC