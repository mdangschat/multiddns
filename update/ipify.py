"""Retrieve public IPv4 address via https://www.ipify.org."""

import json
from urllib.request import Request, urlopen

URL = 'https://api.ipify.org?format=json'


def check_ip():
    # Retrieve HTTP response.
    request = Request(URL)
    response = urlopen(request)
    response_data = response.read().decode()
    # print("Response Data:\n", response_data)

    # Extract IPv4 address as string.
    ip_address = json.loads(response_data)['ip']

    return ip_address


if __name__ == '__main__':
    print(check_ip())
