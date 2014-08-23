# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from optparse import make_option
from django.core.management.base import BaseCommand
from django.utils.timezone import now, datetime
from netactivity.core.capturing import register_session
import subprocess
import fileinput
import re

expression = re.compile('^(?P<hour>\d{2}):(?P<minute>\d{2}):'
                        '(?P<second>\d{2})\.(?P<micro>\d{6})\WIP\W'
                        '(?P<destination>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\.(?P<port>\d{1,5})'
                        '\W(\<|\>)\W'
                        '(?P<source>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\.(?P<d_port>\d{1,5}):')


class Command(BaseCommand):
    """
    Example row:
        09:42:46.466915 IP 10.80.2.25.80 > 10.80.2.108.49434: Flags [S.], seq 1346024167, ack 2536929905, win 28960, options [mss 1460,sackOK,TS val 473206000 ecr 237718194,nop,wscale 7], length 0

        ^                  ^          ^    ^
        time               dest       port client
    """
    option_list = BaseCommand.option_list + (
        make_option('--local-prefix', action='store', type="string", dest='local_prefix', default=None,
                    help='Set your prefix for local network, these destinations will be ignored (Eg. 10.0.0.)'),
        make_option('--iface', action='store', type="string", dest='iface', default=None,
                    help='Network interface to listen on.'),
    )

    help = "Captures network sessions (tcpdump default format)."

    tcpdump_command = "tcpdump 'tcp[13]=18'"

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity'))
        self.local_prefix = options.get('local_prefix')
        self.iface = options.get('iface')

        if self.verbosity >= 1:
            self.stdout.write("Start capturing...")

        try:
            self.capture()
        except KeyboardInterrupt:
            self.stdout.write("shutdown due keyboard interrupt.")

    def capture(self):

        command = self.tcpdump_command
        if self.iface:
            command += " -i %s" % self.iface


        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

        #for line in fileinput.input('-'):
        for line in p.stdout.readlines():
            print line
            r = expression.match(line)
            if r is None:
                self.stderr.write("Wrong input format!")

            today = now()
            hour, min, sec, micro, dest, port, dir, client, dport = r.groups()

            if self.local_prefix and dest.startswith(self.local_prefix):
                if self.verbosity >= 2:
                    self.stdout.write(self.style.NOTICE("Local destination skipped: %s" % dest))
                continue

            hour = int(hour)
            min = int(min)
            sec = int(sec)
            micro = int(micro)
            port = int(port)

            date_captured = datetime(today.year, today.month, today.day,
                                     hour, min, sec, micro)

            register_session(date_captured, client, dest, port)

            if self.verbosity >= 2:
                self.stdout.write(self.style.MIGRATE_SUCCESS("%s > %s:%d" % (client, dest, port)))