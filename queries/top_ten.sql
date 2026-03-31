SELECT wine_id, 
vintages.id AS vintage_id, 
countries.name AS country_name, 
regions.name AS region_name, 
round((price_euros / bottle_volume_ml)*750) AS adjusted_price,
vintages.ratings_average, 
vintages.name, 
vintages.ratings_count, 
vintages.price_euros, 
wines.tannin,
price_discounted_from,  
bottle_volume_ml, 
wines.fizziness
 -- bottle_volume_ml, price_euros, 
FROM  vintages
JOIN wines ON wines.id = vintages.wine_id
JOIN regions ON regions.id =  wines.region_id
JOIN countries ON countries.code = regions.country_code
--JOIN wineries ON wines.winery_id = wineries.id   --  wineries.name AS winery_name
WHERE vintages.ratings_average > 4.7 AND vintages.ratings_count > 100 -- AND adjusted_price < 100 AND adjusted_price > 50  --AND wines.tannin IS NULL --AND vintages.ratings_count < 500 -- 
ORDER BY adjusted_price ASC