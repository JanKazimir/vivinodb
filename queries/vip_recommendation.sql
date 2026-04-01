SELECT grape_id, grapes.name AS grape_name, regions.name AS region_name, regions.country_code, vintages.ratings_average, vintages.name AS vintage_name, vintages.price_euros, vintages.id AS vintage_id, vintages.ratings_count -- wines_count, ratings_count, wines.id,
FROM most_used_grapes_per_country
JOIN grapes on grapes.id = most_used_grapes_per_country.grape_id
JOIN regions on most_used_grapes_per_country.country_code = regions.country_code
JOIN wines on regions.id = wines.region_id
JOIN vintages on vintages.wine_id = wines.id
WHERE grape_id = 2 AND wines.ratings_count > 100
Order BY vintages.ratings_average DESC