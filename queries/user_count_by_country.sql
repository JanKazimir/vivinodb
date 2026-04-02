SELECT name, users_count, wines_count, (users_count/wines_count) AS user_to_wine_ratio,wineries_count,  (users_count/wineries_count) AS user_to_wineries_ratio
FROM countries
ORDER BY user_to_wine_ratio ASC

