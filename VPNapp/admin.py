from django.contrib import admin
from .models import VLAN, IP_address

# Register your models here.

admin.site.register(VLAN)
admin.site.register(IP_address)
