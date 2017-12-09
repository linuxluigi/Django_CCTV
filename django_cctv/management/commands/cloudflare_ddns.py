from django.core.management.base import BaseCommand
import socket

import CloudFlare
from requests import get

from django.conf import settings


def get_external_ip_address():
    """
    Get current external ip address from ipify.org
    """
    ip_address = get('https://api.ipify.org').text

    return ip_address


class Command(BaseCommand):
    help = 'Update external IP address on cloudflare'

    def handle(self, *args, **options):
        # cloudflare login + dns domain name
        target_sub_domain = getattr(settings, "CLOUDFLARE_SUBDOMAIN", None)
        target_zone = getattr(settings, "CLOUDFLARE_ZONE", None)
        cf_email = getattr(settings, "CLOUDFLARE_EMAIL", None)
        cf_token = getattr(settings, "CLOUDFLARE_TOKEN", None)

        # current external ip address
        external_ip_address = get_external_ip_address()

        # A full blown call with passed basic account information
        cf = CloudFlare.CloudFlare(email=cf_email,
                                   token=cf_token,
                                   debug=False)

        # loop every zone in account
        zones = cf.zones.get()
        for zone in zones:

            # if zone name is target_zone -> lookout for target_sub_domain
            if zone['name'] == target_zone:
                # request the DNS records from that zone
                try:
                    dns_records = cf.zones.dns_records.get(zone['id'])
                except CloudFlare.exceptions.CloudFlareAPIError as e:
                    exit('/zones/dns_records.get %d %s - api call failed' % (e, e))

                # loop every dns_records & search for target domain name
                for dns_record in dns_records:
                    if dns_record['name'] == "%s.%s" % (target_sub_domain, target_zone):
                        # delete old entry
                        cf.zones.dns_records.delete(zone['id'], dns_record['id'])

                        break

                # generate new entry
                new_dns_record = {'name': target_sub_domain, 'type': 'A', 'content': external_ip_address,
                                  'proxied': True}
                cf.zones.dns_records.post(zone['id'], data=new_dns_record)

                print("ip updated to %s" % external_ip_address)

                break
