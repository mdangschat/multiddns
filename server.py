#!/usr/local/bin/python3.7

"""
Listener script that awaits a DDNS update and triggers an update for all other DDNS servers.

TODO: Implement Logging.
"""

import time
import ssl
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib import parse

from update.config_loader import get_config
from update.get_ip import get_ip
from update.updater import update_ips

key = b''
update_servers = None


class DDNSHandler(SimpleHTTPRequestHandler):
    # Valid requests contain the basic authorization token and access the path: DOMAIN/?myip=1.2.3.4

    def do_GET(self):
        # print("PATH:", self.path, self.client_address)
        # print("HEADERS:\n", self.headers)
        # print("REQUEST:", self.requestline)

        if self.headers.get('Authorization') is None:
            # print("CASE 2: no auth")
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm=\"Secure Share\"')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Login failed', 'utf-8'))

        elif self.headers.get('Authorization') == 'Basic ' + key.decode('utf-8'):
            if 'myip' in self.path:
                ip_address = parse.parse_qs(parse.urlparse(self.path).query).get('myip')[0]
                print("Update IP:", ip_address)

            else:
                ip_address = get_ip()
                print('"myip" NOT in request, using:', ip_address)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'good %s' % bytes(ip_address, 'utf-8'))

            # Execute update.
            update_ips(update_servers, ip_address)

        else:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm=\"Secure Share\"')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Login failed', 'utf-8'))


def main():
    print('[{}] Starting Multi DDNS Update Server.'.format(time.asctime()))
    global key, update_servers

    server_config, update_servers = get_config('config.json')

    # Initial IP update.
    update_ips(update_servers, get_ip())

    key = server_config['credentials']

    # Setup server.
    httpd = ThreadingHTTPServer(('', server_config['port']), DDNSHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   keyfile=server_config['key'],
                                   certfile=server_config['cert'],
                                   server_side=True)

    # Run server.
    httpd.serve_forever()


if __name__ == '__main__':
    main()
