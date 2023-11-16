from django.urls import path

from . import views

urlpatterns = [
    #ex: /VPNapp/
    path("", views.index, name="index"),
    #ex: /VPNapp/5/
    path("<int:vlan_id>/", views.detail, name="detail"),
    #ex: /VPNapp/login
    path('login/',views.logInView,name='login'),
    #ex: /VPNapp/admin
    path('superuser/',views.adminView,name='admin'),
    #ex: /VPNapp/tryLogIn
    path('tryLogIn/',views.login,name='tryLogIn'),
    #ex: /VPNapp/user
    path('user/',views.userView,name='user'),
    #ex: /VPNapp/register
    path('register/',views.register,name='register'),
    #ex: /VPNapp/restrictVLAN
    path('restrictVLAN/',views.restrictVLAN,name='restrictVLAN'),
    #ex: /VPNapp/restrictUser
    path('restrictUser/',views.restrictUser,name='restrictUser'),
    #ex: /close
    path('close',views.close,name='close'),

    
]