SELECT  wines.name, wines.region_id, winery_id, regions.name AS region_name, country_code
FROM wines
join regions on regions.id = wines.region_id
Where winery_id IN (42463, 7892, 223950)