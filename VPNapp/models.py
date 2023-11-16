from django.db import models

# Create your models here.

class VLAN(models.Model):
    vlan_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.vlan_id)
    
class IP_address(models.Model):
    ip_address = models.CharField(max_length=15, primary_key=True)
    
    def __str__(self):
        return self.ip_address
