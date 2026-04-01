SELECT AVG(ratings_average),  country_code, countries.name AS country_name, Count(wines.id) --ratings_count,  wines.id, wines.name, region_id, regions.name AS region_name,
FROM wines
JOIN regions on wines.region_id  = regions.id
JOIN countries on countries.code = regions.country_code
group by country_code 
HAVING count(wines.id) > 5
order by AVG(ratings_average) DESC -- COunt(wines.id) --