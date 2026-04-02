SELECT grape_id, grapes.name AS grape_name, regions.country_code, ratings_average, wines.name, wines.id -- wines_count, ratings_count,
FROM most_used_grapes_per_country
    JOIN grapes on grapes.id = most_used_grapes_per_country.grape_id
    JOIN regions on most_used_grapes_per_country.country_code = regions.country_code
    JOIN wines on regions.id = wines.region_id
WHERE grape_id = 2 AND ratings_count > 100
Order BY ratings_average DESC