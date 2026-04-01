SELECT wines.id AS wine_id, wines.name AS wine_name, keyword_id, group_name, keyword_type, count as Keyword_count, keywords.name AS keyword_name -- user_structure_count,
FROM wines
JOIN keywords_wine on wines.id = keywords_wine.wine_id
JOIN keywords on keywords.id = keywords_wine.keyword_id
WHERE wines.id = 18931 AND  keyword_type = "primary" AND keyword_name in ("coffee", "toast", "green apple", "cream", "citrus") --AND Keyword_count > 10