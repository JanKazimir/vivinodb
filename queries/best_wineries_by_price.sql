SELECT 
winery_id,
countries.name AS country, 
regions.name AS region,
--round((price_euros / bottle_volume_ml)*750) AS adjusted_price,
(AVG(vintages.ratings_average) / AVG(round((price_euros / bottle_volume_ml)*750))) AS bang_for_buck,
round(AVG(vintages.price_euros)) AS avg_price, 
vintages.bottle_volume_ml
FROM vintages
JOIN wines ON wines.id = vintages.wine_id
JOIN regions ON regions.id =  wines.region_id
JOIN countries ON countries.code = regions.country_code
WHERE  vintages.ratings_count > 100 
GROUP BY wines.winery_id
-- HAVING 
ORDER BY bang_for_buck DESC