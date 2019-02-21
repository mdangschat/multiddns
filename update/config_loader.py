"""
Read and parse the `config.json` file from the repository root.
"""

import base64
import json
import os


def get_config(filename):
    base_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    json_path = os.path.join(base_path, filename)
    assert os.path.exists(json_path) and os.path.isfile(json_path)

    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
        server_config = data['server']
        update_servers = data['update_servers']

    for server in update_servers:
        server['password'] = __decode(server['password'], None)

        # Base64 encode the `USERNAME:LOGIN` credentials.
        __add_credentials(server)

    __add_credentials(server_config)

    return server_config, update_servers


def __add_credentials(server):
    # Base64 encode the `USERNAME:LOGIN` credentials.
    credentials = '{0:s}:{1:s}'.format(server['username'], server['password'])
    del server['username']
    del server['password']
    credentials = base64.b64encode(bytes(credentials, 'utf-8'))
    server['credentials'] = credentials


def __decode(entry, key):
    del key
    return entry


if __name__ == '__main__':
    print(get_config('config.json'))
