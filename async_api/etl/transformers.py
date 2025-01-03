class TransformerMovies:
    FIELEDS = ['id', 'title', 'description', 'rating', 'person_ids', 'roles', 'full_names', 'genres']

    async def start(self, data):
        to_return = {}
        for d_list in data:
            d = {key: value for key, value in zip(self.FIELEDS, d_list)}
            d['id'] = str(d['id'])
            d['person_ids'] = [str(uuid) for uuid in d['person_ids']]

            to_return[d['id']] = {
                'id': d['id'],
                'imdb_rating': d['rating'],
                'title': d['title'],
                'description': d['description'],
                'genres': d['genres'],
                'directors_names': [],
                'actors_names': [],
                'writers_names': [],
                'directors': [],
                'actors': [],
                'writers': [],
            }

            for (person_id, person_role, person_name) in zip(d['person_ids'], d['roles'], d['full_names']):
                if person_role is None or person_name is None:
                    continue
                to_return[d['id']][f'{person_role}s_names'].append(person_name)

                to_return[d['id']][f'{person_role}s'].append({'id': person_id, 'name': person_name})

        return to_return

class TransformerPersons:
    FIELDS = ['id', 'name']

    async def start(self, data):
        res = {}
        for item in data:
            d = {key: value for key, value in zip(self.FIELDS, item)}
            d['id'] = str(d['id'])
            res[d['id']] = {
                'id': d['id'],
                'name': d['name'],
            }
        return res

class TransformerGenres:
    FIELEDS = ['id', 'name', 'description']

    async def start(self, data):
        to_return = {}
        for d_list in data:
            d = {key: value for key, value in zip(self.FIELEDS, d_list)}
            d['id'] = str(d['id'])
            to_return[d['id']] = {
                'id': d['id'],
                'name': d['name'],
                'description': d['description'],
            }

        return to_return
