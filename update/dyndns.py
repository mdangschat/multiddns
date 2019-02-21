"""Retrieve public IPv4 address via http://checkip.dyndns.org."""

import re
from urllib.request import Request, urlopen

URL = 'http://checkip.dyndns.org/'


def check_ip():
    # Retrieve HTTP response.
    request = Request(URL)
    response = urlopen(request)
    response_data = response.read().decode()
    # print("Response Data:\n", response_data)

    # Extract IPv4 address as string.
    pattern = re.compile(r'<body>[A-Za-z ]+: (.+)</body>')
    ip_address = re.findall(pattern, response_data)[0]

    return ip_address


if __name__ == '__main__':
    print(check_ip())
