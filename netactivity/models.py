from django.utils.timezone import now
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=64, null=True, default=None)
    mac_address = models.CharField(max_length=20, unique=True)
    last_ip_address = models.GenericIPAddressField(null=True, default=None, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_ip_update = models.DateTimeField(null=True, default=None)

    def __unicode__(self):
        return self.name if self.name is not None else self.mac_address


class TargetHost(models.Model):
    FLAG = (
        ('unknown', 'unknown'),
        ('known', 'known'),
        ('trusted', 'trusted'),
        ('advertiser', 'advertiser'),
        ('unwanted', 'unwanted'),
        ('harmful', 'harmful'),
    )
    name = models.CharField(max_length=64, null=True, default=None)
    ip_address = models.GenericIPAddressField(unique=True)
    reverse_dns = models.CharField(max_length=255, null=True, default=None)
    location = models.CharField(max_length=2, null=True, default=None)
    flag = models.CharField(max_length=32, choices=FLAG)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if self.reverse_dns is not None:
            return "%s (%s)" % (self.reverse_dns, self.ip_address)

        return self.ip_address


class DNSElement(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    clients = models.ManyToManyField(Client, related_name='dns_requests')
    target_hosts = models.ManyToManyField(TargetHost, related_name='dns_names')
    last_query = models.DateTimeField(null=True, default=None)

    def __unicode__(self):
        return self.domain


class NetSession(models.Model):
    client = models.ForeignKey(Client, related_name='net_connections')
    target_host = models.ForeignKey(TargetHost, related_name='net_connections')
    port = models.PositiveIntegerField()
    protocol = models.CharField(max_length=32, null=True, default=None)
    date_created = models.DateTimeField(default=now)