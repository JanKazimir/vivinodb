SELECT wines.id AS wine_id, vintages.id AS vintage_id, count(vintages.id) AS count, wines.ratings_average AS wine_average, wines.winery_id, AVG(vintages.ratings_average) AS vintage_average
FROM wines 
JOIN vintages on wines.id = vintages.wine_id
GROUP BY wines.id
HAVING count > 5
ORDER BY wines.ratings_average DESC