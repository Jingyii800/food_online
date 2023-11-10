from django.contrib import admin

from menu.models import Category, FoodItem

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    # automatically generate slug
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name','vendor',  'updated_at')
    search_fields = ('category_name', 'vendor__vendor_name') # search by names

class FooditemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_title',)}
    list_display = ('food_title', 'vendor', 'price', 'is_available', 'updated_at')
    search_fields = ('food_title', 'category__category_name', 'vendor__vendor_name', 'price')
    list_filter = ('is_available',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FooditemAdmin)