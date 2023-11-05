from django.urls import path
from . import views

urlpatterns = [
    path('userRegister', views.userRegister, name='userRegister'),
    path('vendorRegister', views.vendorRegister, name='vendorRegister')
]
