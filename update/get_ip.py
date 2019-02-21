import update.ipify
import update.dyndns
import update.whatsmyipaddress


def get_ip():
    services = [
        update.ipify.check_ip,
        update.whatsmyipaddress.check_ip,
        update.dyndns.check_ip
    ]

    ip_address = services[0]()
    return ip_address
