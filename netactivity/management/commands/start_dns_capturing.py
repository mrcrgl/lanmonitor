# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from netactivity.models import DNSElement, Client, TargetHost
import subprocess
import re
import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = "Foo."

    tail_command = "tail -f /var/log/dnsmasq.log"

    cache = {}
    current_query = ""

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity'))

        try:
            self.capture()
        except KeyboardInterrupt:
            self.stdout.write("Keyboard Interrupted")

    def capture(self):

        logger.info("Start DNS capturing")
        p = subprocess.Popen(self.tail_command, shell=True, stdout=subprocess.PIPE)

        while True:
            line = p.stdout.readline()

            if not line:
                logger.warning("empty line... process terminates")
                break

            line = line.rstrip()
            b, log = line.split("dnsmasq")

            try:
                cmd_type = ""
                pid, cmd, host, rel, client_ip = log.split()
                pid = pid[1:-2]

                if cmd.endswith("]"):
                    cmd, cmd_type = re.match('^([a-z]+)\[([A-Z]+?)\]$', cmd)

            except KeyError:
                continue

            if self.current_query != host and cmd == 'query':
                # Clear cache, set new
                self.save_cache()

                self.cache = {
                    'date': now(),
                    'client_ip': client_ip,
                    'type': cmd_type,
                    'host': host,
                    'replies': []
                }
                self.current_query = host

            if self.current_query == host and cmd == 'reply':
                if 'replies' in self.cache.keys():
                    self.cache['replies'].append(client_ip)

            # Append data

    def save_cache(self):
        date = self.cache.get('date', None)
        client_ip = self.cache.get('client_ip', None)
        type = self.cache.get('type', None)
        host = self.cache.get('host', None)
        replies = self.cache.get('replies', None)

        if date and client_ip and type and host and replies:
            # all fine
            client, c = Client.objects.get_or_create(last_ip_address=client_ip)

            targets = []
            for reply in replies:
                target, c = TargetHost.objects.get_or_create(ip_address=reply)
                targets.append(target)

            dns, created = DNSElement.objects.get_or_create(domain=host, type=type.upper())

            dns.last_query = now()

            if not created:
                dns.target_hosts.clear()

            dns.clients.add(client)
            dns.target_hosts.add(*targets)
            dns.save()

        else:
            logger.warning("Invalid cache content: %r", self.cache)