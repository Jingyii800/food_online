from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 
                    'username', 'role', 'is_active')
    ordering = ('-date_joined',) # order of dispaly
    filter_horizontal = () 
    list_filter = ()
    fieldsets = ()

admin.site.register(User, CustomUserAdmin)