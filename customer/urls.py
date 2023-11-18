from . import views
from django.urls import path
from accounts import views as AccountsViews

urlpatterns = [
    path('', AccountsViews.custDashboard, name='customer'),
    path('profile/', views.c_profile, name='c_profile'),
]