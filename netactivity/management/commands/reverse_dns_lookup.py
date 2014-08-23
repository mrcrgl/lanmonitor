# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from netactivity.utils.dns import reverse_dns_lookup


class Command(BaseCommand):

    help = "Foo."
    args = "ip address [ip address] ..."

    def handle(self, *args, **options):

        if len(args) < 1:
            raise CommandError("Missing command-line argument (expecting ad least one 'ip address')")

        for ip_address in args:
            self.stdout.write("IP address '%s' PTR is '%s'" % (ip_address, reverse_dns_lookup(ip_address)))