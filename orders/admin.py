from django.contrib import admin

from orders.models import Order, OrderedItems, Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_id', 'payment_method', 'amount', 'status']

class OrderedItemInline(admin.TabularInline):
    model = OrderedItems
    readonly_fields = ('order','user','fooditem','payment','quantity','price','amount')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment', 'order_number', 
                    'total','address', 'payment', 'status', 'is_ordered']
    inlines = [OrderedItemInline]

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedItems)


