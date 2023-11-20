from . import views
from django.urls import path
from accounts import views as AccountsViews

urlpatterns = [
    path('', AccountsViews.custDashboard, name='customer'),
    path('profile/', views.c_profile, name='c_profile'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_detail/<int:order_number>', views.order_detail, name='order_detail')
]