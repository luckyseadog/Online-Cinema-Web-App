RAW_PERSONS = '''
SELECT p.id,
       p.full_name,
       p.modified
FROM content.person p
WHERE p.modified >= %s AND p.modified < %s
'''

WHERE_CLAUSE_MODIFIED = "fw.modified >= '%s' AND fw.modified < '%s'"

WHERE_CLAUSE_IN = 'fw.id IN ({})'

FILM_IDS_BY_GENRE = '''SELECT DISTINCT fw.id
FROM content.genre g
LEFT JOIN content.genre_film_work gfw ON gfw.genre_id = g.id
LEFT JOIN content.film_work fw ON fw.id = gfw.film_work_id
WHERE g.modified >= %s AND g.modified < %s
'''

FILM_IDS_BY_PERSON = '''SELECT DISTINCT fw.id
FROM content.person p
LEFT JOIN content.person_film_work pfw ON p.id = pfw.person_id
LEFT JOIN content.film_work fw ON fw.id = pfw.film_work_id
WHERE p.modified >= %s AND p.modified < %s
'''

EXTRUCT = '''SELECT
    subquery.id,
    subquery.title,
    subquery.description,
    subquery.rating,
    subquery.person_ids,
    subquery.roles,
    subquery.full_names,
    ARRAY_AGG(g.name) AS genres
FROM (
    SELECT
        fw.id,
        fw.title,
        fw.description,
        fw.rating,
        ARRAY_AGG(p.id) as person_ids,
        ARRAY_AGG(pfw.role) AS roles,
        ARRAY_AGG(p.full_name) AS full_names
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    WHERE {}
    GROUP BY fw.id, fw.title, fw.description, fw.rating
) AS subquery
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = subquery.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
GROUP BY subquery.id,
         subquery.title,
         subquery.description,
         subquery.rating,
         subquery.person_ids,
         subquery.roles,
         subquery.full_names
ORDER BY subquery.title
'''

RAW_GENRE_EXTRUCT = '''SELECT
    g.id,
    g.name,
    g.description
FROM content.genre g
WHERE g.modified >= %s AND g.modified < %s
'''
