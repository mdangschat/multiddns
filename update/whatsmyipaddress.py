"""Retrieve public IPv4 address via http://ipv4bot.whatismyipaddress.com/."""

from urllib.request import Request, urlopen

URL = 'http://ipv4bot.whatismyipaddress.com/'


def check_ip():
    # Retrieve HTTP response.
    request = Request(URL)
    response = urlopen(request)
    response_data = response.read().decode()
    # print("Response Data:\n", response_data)

    # Extract IPv4 address as string.
    ip_address = response_data.strip()

    return ip_address


if __name__ == '__main__':
    print(check_ip())
