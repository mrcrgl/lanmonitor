# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from netactivity.utils.net import format_hw_address
from django.utils.timezone import now
from netactivity.models import Client
import re
import subprocess
import time

ip_expression = re.compile('.*\((?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)')
mac_expression = re.compile(
    '.*\W(?P<mac>[0-9a-f]{1,2}:[0-9a-f]{1,2}:[0-9a-f]{1,2}:[0-9a-f]{1,2}:[0-9a-f]{1,2}:[0-9a-f]{1,2})'
)


class Command(BaseCommand):

    help = "Foo."

    arp_command = "arp -an"
    last_result_length = 0
    cache = {}

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity'))
        self.frequency = 1

        # print mac_expression.match('Hallo du sack! 12:12:12:12:12:12 foo bar')
        try:
            while True:
                self.call_arp_table()
                time.sleep(self.frequency)
        except KeyboardInterrupt:
            self.stdout.write("Keyboard Interrupted")

    def call_arp_table(self):
        p = subprocess.Popen(self.arp_command, shell=True, stdout=subprocess.PIPE)
        output, errors = p.communicate()
        output_size = len(output)

        if output_size != self.last_result_length:
            self.last_result_length = output_size

            for i in output.split("\n"):
                if not i:
                    continue

                ip_res = ip_expression.match(i)
                mac_res = mac_expression.match(i)

                if ip_res is None:
                    self.stderr.write("Invalid format (ip): '%s'" % i)
                    continue

                if mac_res is None:
                    self.stderr.write("Invalid format (mac): '%s'" % i)
                    continue

                ip = ip_res.group(1)
                mac = format_hw_address(mac_res.group(1))

                print "%s -> %s" % (mac, ip)
                # Check if update is required
                if ip not in self.cache.keys() or mac != self.cache[ip]:
                    if self.verbosity >= 2:
                        self.stdout.write("Update required for ip '%s'@'%s'" % (ip, mac))

                    mac_matched = Client.objects.filter(mac_address=mac).first()

                    l = Client.objects.filter(last_ip_address=ip).first()
                    if l:
                        if mac_matched and mac_matched.pk != l.pk:
                            # remove ip, there's a new client
                            l.last_ip_address = None
                            l.save()
                        else:
                            l.mac_address = mac
                            l.last_ip_update = now()
                            l.save
                    else:
                        c, created = Client.objects.get_or_create(mac_address=mac, defaults={
                            'last_ip_update': now(),
                            'last_ip_address': ip
                        })

                        if not created:
                            c.last_ip_update = now()
                            c.last_ip_address = ip
                            c.save()

                # Add/Update cache
                self.cache[ip] = mac
