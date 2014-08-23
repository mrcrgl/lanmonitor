from django.contrib import admin
from .models import *


class ClientAdmin(admin.ModelAdmin):
    model = Client

    list_display = ('display_name', 'name', 'last_ip_address', 'last_ip_update', 'date_created')

    def display_name(self, instance):
        return unicode(instance)


class NetSessionAdmin(admin.ModelAdmin):

    list_display = ('id', 'client', 'target_host', 'port', 'date_created',)
    search_fields = ('client__mac_address', 'target_host__name', 'client__name', 'port',)
    raw_id_fields = ('target_host', 'client',)
    readonly_fields = ('date_created', )
    ordering = ['-date_created']


class TargetHostAdmin(admin.ModelAdmin):

    list_display = ('name', 'ip_address', 'reverse_dns', 'location', 'flag',)
    search_fields = ('name', 'ip_address', 'reverse_dns', 'location')
    list_filter = ('flag',)
    readonly_fields = ('ip_address', 'reverse_dns', 'location',)

# Register your models here.
admin.site.register(Client, ClientAdmin)
admin.site.register(TargetHost, TargetHostAdmin)
admin.site.register(NetSession, NetSessionAdmin)
admin.site.register(DNSElement)