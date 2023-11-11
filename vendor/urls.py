from django.urls import path
from . import views
from accounts import views as accountViews
urlpatterns = [
    path('', accountViews.vendorDashboard, name='vendor'),
    path('profile/', views.v_profile, name ='v_profile'),
    path('menu-builder/', views.menu_builder, name = 'menu_builder'),
    path('menu-builder/category/<int:pk>/', views.fooditems_by_category, 
         name = 'fooditems_by_category'),

    # category CRUD create read update delete
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>', views.delete_category, name='delete_category'),

    # food item CRUD 
    path('menu-builder/fooditem/add', views.add_fooditem, name='add_fooditem'),
    path('menu-builder/fooditem/edit/<int:pk>', views.edit_fooditem, name='edit_fooditem'),
    path('menu-builder/fooditem/delete/<int:pk>', views.delete_fooditem, name='delete_fooditem'),
]