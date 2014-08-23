from __future__ import unicode_literals
from .utils.geolocation import geo_ip_lookup
from .utils.dns import reverse_dns_lookup
from distributed_task import register_task

import logging
logger = logging.getLogger(__name__)


@register_task
def enrich_target_host(instance):

    if not instance.reverse_dns:
        instance.reverse_dns = reverse_dns_lookup(instance.ip_address)

    if not instance.location:
        instance.location = geo_ip_lookup(instance.ip_address)

    if not instance.name and instance.reverse_dns:
        name = instance.reverse_dns

        if instance.location:
            name += " (%s)" % instance.location

        instance.name = name

    instance.save()