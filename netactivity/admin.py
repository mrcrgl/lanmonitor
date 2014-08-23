from django.contrib import admin
from .models import *


class ClientAdmin(admin.ModelAdmin):
    model = Client

    list_display = ('mac_address', 'name', 'last_ip_address', 'last_ip_update', 'date_created')

# Register your models here.
admin.site.register(Client, ClientAdmin)
admin.site.register(TargetHost)
admin.site.register(NetSession)
admin.site.register(DNSElement)