select AVG(ratings_count), ratings_average
FROM wines
group by ratings_average
