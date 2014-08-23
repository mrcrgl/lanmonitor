from django.conf import settings
import pygeoip
import os

GEO_DATABASE = os.path.join(settings.ASSETS_DIR, 'GeoIP.dat')

gi = pygeoip.GeoIP(GEO_DATABASE)


def geo_ip_lookup(ip_address):
    country = gi.country_code_by_addr(ip_address)

    if not country:
        return None

    return country