# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from netactivity.utils.geolocation import geo_ip_lookup


class Command(BaseCommand):

    help = "Foo."
    args = "ip address [ip address] ..."

    def handle(self, *args, **options):

        if len(args) < 1:
            raise CommandError("Missing command-line argument (expecting ad least one 'ip address')")

        for ip_address in args:
            self.stdout.write("IP address '%s' belongs to '%s'" % (ip_address, geo_ip_lookup(ip_address)))