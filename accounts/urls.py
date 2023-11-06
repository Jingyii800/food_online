from django.urls import path
from . import views

urlpatterns = [
    path('userRegister', views.userRegister, name='userRegister'),
    path('vendorRegister', views.vendorRegister, name='vendorRegister'),

    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    
    path('myAccount', views.myAccount, name='myAccount'),
    path('custDashboard', views.custDashboard, name='custDashboard'),
    path('vendorDashboard', views.vendorDashboard, name='vendorDashboard'),
]
