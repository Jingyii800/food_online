from django.contrib import admin
from vendor.models import OpeningHour, Vendor

class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'vendor_name') # click on vendor_name will take to user
    list_editable =('is_approved',)
# Register your models here.
admin.site.register(Vendor, VendorAdmin)

class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'day', 'start_hour', 'end_hour', 'is_closed')
admin.site.register(OpeningHour)