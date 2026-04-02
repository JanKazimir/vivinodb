SELECT 
  winery_id,
  avg_rating,
  avg_price,
  (avg_rating - MIN(avg_rating) OVER()) / (MAX(avg_rating) OVER() - MIN(avg_rating) OVER()) AS norm_rating,
  (avg_price - MIN(avg_price) OVER()) / (MAX(avg_price) OVER() - MIN(avg_price) OVER()) AS norm_price,
  (avg_rating - MIN(avg_rating) OVER()) / (MAX(avg_rating) OVER() - MIN(avg_rating) OVER()) - (avg_price - MIN(avg_price) OVER()) / (MAX(avg_price) OVER() - MIN(avg_price) OVER()) AS bang_for_buck
FROM (
  SELECT winery_id, AVG(vintages.ratings_average) AS avg_rating, AVG(price_euros) AS avg_price
  FROM vintages JOIN wines ON wines.id = vintages.wine_id
  GROUP BY winery_id
  HAVING COUNT(*) > 5
)