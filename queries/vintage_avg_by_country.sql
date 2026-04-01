SELECT AVG(vintages.ratings_average),  country_code, countries.name AS country_name, COUNT(vintages.id) AS vintages_count --ratings_count,  wines.id, wines.name, region_id, regions.name AS region_name,
FROM wines
JOIN vintages on wines.id = vintages.wine_id
JOIN regions on wines.region_id  = regions.id
JOIN countries on countries.code = regions.country_code
group by country_code 
HAVING COUNT(vintages.id) > 5
ORDER BY AVG(vintages.ratings_average) DESC