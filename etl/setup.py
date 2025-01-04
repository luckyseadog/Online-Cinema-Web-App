import requests


def setup(elastic_host, elastic_port, index, data_json):
    res = requests.head(f'http://{elastic_host}:{elastic_port}/{index}')

    if res.status_code != 200:
        with open(data_json) as f:
            data = f.read()
        headers = {'Content-Type': 'application/json'}
        res = requests.put(f'http://{elastic_host}:{elastic_port}/{index}', headers=headers, data=data)
