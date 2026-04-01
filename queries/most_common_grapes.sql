SELECT grape_id, name, wines_count
FROM most_used_grapes_per_country
JOIN grapes on grapes.id = most_used_grapes_per_country.grape_id
group BY grape_id
ORDER BY wines_count DESC