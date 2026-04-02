SELECT vintages_per_wine, COUNT(*) AS number_of_wines
FROM (
    SELECT wines.id, wines.name, COUNT(*) AS vintages_per_wine
    FROM wines
    JOIN vintages ON wines.id = vintages.wine_id
    GROUP BY wines.id, wines.name
) AS t
GROUP BY vintages_per_wine
ORDER BY vintages_per_wine ASC;


--SELECT  wines.name, vintages.wine_id, count(wines.id) AS count_of_vintages_per_wine--count(count(wines.id)) AS count_of_count --wines.id,
--FROM wines
--JOIN vintages on wines.id = vintages.wine_id
--GROUP BY wines.id --count(wines.id)
--HAVING count(wines.id) >=2 -- AND count(wines.id) < 7 
--ORDER BY count(wines.id) DESC