from django.core.management.base import BaseCommand
import socket

import CloudFlare

from django.conf import settings


def get_external_ip_address():
    """
    Get current external ip address from open dns server
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("208.67.222.222", 80))  # open dns server
    ip_address = s.getsockname()[0]
    s.close()

    return ip_address


class Command(BaseCommand):
    help = 'Update external IP address on cloudflare'

    def handle(self, *args, **options):
        # cloudflare login + dns domain name
        target_sub_domain = getattr(settings, "CLOUDFLARE_ZONE", None)
        target_zone = getattr(settings, "CLOUDFLARE_SUBDOMAIN", None)
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
                        dns_record['content'] = external_ip_address

                        # delete old entry
                        cf.zones.dns_records.delete(zone['id'], dns_record['id'])

                        # generate new entry
                        cf.zones.dns_records.post(zone['id'], data=dns_record)

                        print("ip updated to %s" % external_ip_address)

                        break
                break
