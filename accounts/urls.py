from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.myAccount),
    path('userRegister', views.userRegister, name='userRegister'),
    path('vendorRegister', views.vendorRegister, name='vendorRegister'),

    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    
    path('myAccount', views.myAccount, name='myAccount'),
    path('custDashboard/', views.custDashboard, name='custDashboard'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    
    path('vendor/', include('vendor.urls') ),
    path('customer/', include('customer.urls')),
]
