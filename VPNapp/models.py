from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class VLAN(models.Model):
    vlan_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.vlan_id)
    
class IP_address(models.Model):
    ip_address = models.CharField(max_length=15, primary_key=True)
    
    def __str__(self):
        return self.ip_address

class UserBelongsToVLAN(models.Model):
    #with a many to one relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    vlan = models.ForeignKey(VLAN, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user) + " " + str(self.vlan)
        
class UserRestrictedIP(models.Model):
    #with a many to many relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IP_address, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('user', 'ip_address'),)

    def __str__(self) -> str:
        return str(self.user.username) + " " + str(self.ip_address)
    
    
    
class VLANRestrictedIP(models.Model):
    #with a many to many relationship
    vlan = models.ForeignKey(VLAN, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IP_address, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('vlan', 'ip_address'),)
    
    def __str__(self) -> str:
        return str(self.vlan) + " " + str(self.ip_address)


    
    
    

