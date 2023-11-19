from django.contrib import admin

from marketplace.models import Cart, Tax

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'fooditem','quantity', 'updated_at')

admin.site.register(Cart, CartAdmin)

class TaxAdmin(admin.ModelAdmin):
    prepopulated_fields = {'tax_slug': ('tax_type',)}
    list_display = ('tax_type', 'tax_percentage', 'is_active' )
    
admin.site.register(Tax, TaxAdmin)