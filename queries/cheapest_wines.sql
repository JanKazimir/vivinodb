SELECT wine_id, vintages.name, vintages.id AS vintage_id, regions.name AS region_name, countries.name AS country_name, vintages.ratings_average, vintages.ratings_count, vintages.price_euros, price_discounted_from,  bottle_volume_ml, wines.tannin, round((price_euros / bottle_volume_ml)*750) AS adjusted_price -- bottle_volume_ml, price_euros, 
FROM  vintages
JOIN wines ON wines.id = vintages.wine_id
JOIN regions ON regions.id =  wines.region_id
JOIN countries ON countries.code = regions.country_code
--JOIN wineries ON wines.winery_id = wineries.id   --  wineries.name AS winery_name
WHERE vintages.ratings_average > 3. AND vintages.ratings_count > 100 --AND wines.tannin IS NULL --AND vintages.ratings_count < 500 -- 
ORDER BY adjusted_price ASC

-- cheapest wines: Nothing below 21 for 750 ml. 