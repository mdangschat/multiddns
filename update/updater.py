"""
Updates a set of DDNS servers.
"""

import time
from urllib.request import Request, urlopen

from update.config_loader import get_config
from update.get_ip import get_ip


def update_ips(servers, ip_address):
    for server in servers:
        update_ip(server, ip_address)


def update_ip(server, ip):
    update_url = server['update_url'].format(ip=ip)

    request = Request(update_url)
    request.add_header('Authorization', 'Basic {:s}'.format(server['credentials'].decode('utf-8')))

    response = urlopen(request).read().decode()
    assert response == 'good {ip:s}'.format(ip=ip)
    print('[{}] Submitted {:s} for {:s}'.format(time.asctime(), ip, server['name']))


if __name__ == '__main__':
    server_config, update_servers = get_config('config.json')
    __ip = get_ip()

    # Update servers directly.
    # update_ips(update_servers, __ip)

    # Update servers via the update server.
    # update_ip(server_config, __ip)

    # Update servers via the local update server.
    server_config['update_url'] = 'http://localhost:48234/?myip={ip:s}'
    update_ip(server_config, __ip)
