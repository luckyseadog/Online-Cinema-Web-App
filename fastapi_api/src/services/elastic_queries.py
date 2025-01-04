GET_ALL_FILMS = '''{
  "from": %s,
  "size": %s,
  "query": {
    "match_all": { }
  },
  "sort": [
    {
      "imdb_rating": "%s"
    }
  ]
}'''

GET_ALL_FILMS_IN_GENRE = '''{
  "from": %s,
  "size": %s,
  "query": {
    "terms": {
      "genres": [ "%s" ]
    }
  },
  "sort": [
    {
      "imdb_rating": "%s"
    }
  ]
}'''

SEARCH_FILMS = '''{
    "from": %s,
    "size": %s,
    "query": {
        "match": {
            "title": {
                "query": "%s",
                "fuzziness": "auto"
            }
        }
    },
    "sort": [
    {
      "_score": "desc"
    }
  ]
}'''


GET_GENRE_BY_NAME = '''{
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "name": "%s"
                    }
                }
            ]
        }
    }
}'''

GET_PERSON_FILMS_AND_ROLES = '''{
  "from": %s,
  "size": %s,
  "query": {
    "bool": {
      "should": [
        {
          "nested": {
            "path": "actors",
            "query": {"bool": {"should": {"term": {"actors.id": "%s"}}}}
          }
        },
        {
          "nested": {
            "path": "directors",
            "query": {"bool": {"should": {"term": {"directors.id": "%s"}}}}
          }
        },
        {
          "nested": {
            "path": "writers",
            "query": {"bool": {"should": {"term": {"writers.id": "%s"}}}}
          }
        }
      ]
    }
  }
}'''


PERSON_SEARCH = '''{
  "query": {
    "match": {
      "name": {
        "query": "%s",
        "fuzziness": "auto"
      }
    }
  }
}'''
