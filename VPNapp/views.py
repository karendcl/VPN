from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout

# Create your views here.

def index(request):
    return render(request, "login.html")

def detail(request, vlan_id):

    response = "You're looking at vlan %s"
    return HttpResponse(response % vlan_id)

def adminView(request):
    #redirect to /superuser
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, "admin.html")
        else:
            return render(request, "user.html")
    
    return render(request, "user.html")

def logInView(request):
    #log out
    if request.user.is_authenticated:
        #log out the user
        logout(request)

    return render(request, "login.html")

def userView(request):
    if request.user.is_authenticated:
        return render(request, "user.html")
    return logInView()



def CreateVLAN(vlan_id) -> VLAN:
    #check if vlan exists
    vlan_id = int(vlan_id)
    if VLAN.objects.filter(vlan_id=vlan_id).exists():
        return VLAN.objects.filter(vlan_id=vlan_id).first()
    #create vlan
    vlan = VLAN(vlan_id=vlan_id)
    vlan.save()
    return vlan

def CreateUserBelongsToVLAN(user,vlan):
    #check if user belongs to vlan exists
    if UserBelongsToVLAN.objects.filter(user=user, vlan=vlan).exists():
        return UserBelongsToVLAN.objects.filter(user=user, vlan=vlan).first()
    #create user belongs to vlan
    userBelongsToVLAN = UserBelongsToVLAN(user=user, vlan=vlan)
    userBelongsToVLAN.save()
    return userBelongsToVLAN

def CreateUser(username, password, vlan) -> User:
    #chech if user exists
    if User.objects.filter(username=username).exists():
        return User.objects.filter(username=username).first()
    #create user
    user = User.objects.create_user(username=username, password=password, email=None)
    user.save()

    vlanObj = CreateVLAN(vlan)

    #create user belongs to vlan
    userBelongsToVLAN = CreateUserBelongsToVLAN(user, vlanObj)

    return user

def CreateIP(ip_address) -> IP_address:
    #check if ip exists
    if IP_address.objects.filter(ip_address=ip_address).exists():
        return IP_address.objects.filter(ip_address=ip_address).first()
    #create ip
    ip = IP_address(ip_address=ip_address)
    ip.save()
    return ip

def register(request):
    if request.method == "POST":
        #get username and password
        username = request.POST['username']
        password = request.POST['password']
        vlan = request.POST['vlan']
        #create user
        CreateUser(username, password, vlan)
        #redirect to login
    return render(request, 'admin.html')
    
def login(request):
    #if request is post
    if request.method == "POST":
        #get username and password
        username = request.POST['username']
        password = request.POST['password']
        protocol = request.POST['protocol']

    
        #check if user exists
        user = authenticate(username=username, password=password)
        


        if user is not None:
            #see if user is superadmin
            if user.is_superuser:
                #redirect to /VPNapp/admin
                return render(request, 'admin.html')

            #redirect to /VPNapp/admin
            return render(request, 'user.html', {'protocol': protocol})
        

   
    return render(request, 'login.html')
    
def CreateVlanRestr(vlan, ip):
    #check if vlanrestricted exists
    if VLANRestrictedIP.objects.filter(vlan=vlan, ip_address=ip).exists():
        return VLANRestrictedIP.objects.filter(vlan=vlan, ip_address=ip).first()
    #create vlanrestricted
    vlanRestricted = VLANRestrictedIP(vlan=vlan, ip_address=ip)
    vlanRestricted.save()
    return vlanRestricted

def CreateUserRestricted(user, ip):
    #check if userrestricted exists
    if UserRestrictedIP.objects.filter(user=user, ip_address=ip).exists():
        return UserRestrictedIP.objects.filter(user=user, ip_address=ip).first()
    #create userrestricted
    userRestricted = UserRestrictedIP(user=user, ip_address=ip)
    userRestricted.save()
    return userRestricted

def restrictVLAN(request):
    if (request.method== "POST"):
        #get ipaddress and vlan
        ip_address = request.POST['ip_address']
        vlan = request.POST['vlan']
        #get ip object
        ipObj = CreateIP(ip_address)
        #get vlan object
        vlanObj = CreateVLAN(vlan)
        #create user belongs to vlan
        vlanRestricted = CreateVlanRestr(vlanObj, ipObj)
        #redirect to /VPNapp/admin
        
    return render(request, 'admin.html')

def restrictUser(request):
    if (request.method== "POST"):
        #get ipaddress and vlan
        ip_address = request.POST['ip_address']
        user = request.POST['username']
        #get ip object
        ipObj = CreateIP(ip_address)
        #get user object
        userObj = CreateUser(user, "password", "1")
        #create user belongs to vlan
        userRestricted = CreateUserRestricted(userObj, ipObj)
        #redirect to /VPNapp/admin
        
    return render(request, 'admin.html')

def close(request):
    return logInView(request)