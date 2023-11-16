from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.

def index(request):
    # vlansList = VLAN.objects.order_by("vlan_id")
    # output = ", ".join([str(v.vlan_id) for v in vlansList])
    
    return render(request, "login.html")

def detail(resquest, vlan_id):
    response = "You're looking at vlan %s"
    return HttpResponse(response % vlan_id)

def adminView(request):
    return render(request, "admin.html")

def logInView(request):
    return render(request, "login.html")

def userView(request):
    return render(request, "user.html")

def login(request):
    #if request is post
    if request.method == "POST":
        #get username and password
        username = request.POST['username']
        password = request.POST['password']

        print(username)
        #check if user exists
        user = authenticate(username=username, password=password)
        


        if user is not None:
            #see if user is superadmin
            if user.is_superuser:
                #redirect to /VPNapp/admin
                return redirect("/VPNapp/admin")

            #redirect to /VPNapp/admin
            return redirect("/VPNapp/user")
        

   
    return redirect("/VPNapp/login")
    

