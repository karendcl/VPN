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
    path('admin/',views.adminView,name='admin'),
    #ex: /VPNapp/tryLogIn
    path('tryLogIn/',views.login,name='tryLogIn'),
    #ex: /VPNapp/user
    path('user/',views.userView,name='user'),

    
]