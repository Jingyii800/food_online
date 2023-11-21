from django.db import models
from accounts.models import User
from menu.models import FoodItem
from vendor.models import Vendor
import json
import ast

request_object = ''

class Payment(models.Model):
    PAYMENT_METHOD = (
        ('PayPal', 'PayPal'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.transaction_id

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled')
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    total = models.FloatField()
    tax_data = models.JSONField(blank=True, null=True, help_text="Data format: {'tax_type':{'tax_percentage':'tax_amount'}}")
    total_tax = models.FloatField()
    # for many to many fields
    vendors = models.ManyToManyField(Vendor, blank=True)
    total_data = models.JSONField(blank=True, null=True)
    payment_method = models.CharField(max_length=25)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # combine first name and last name
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    # display all vendors in this order
    def order_placed_to(self):
        return ",".join( [i.vendor_name for i in self.vendors.all()])
    
    def get_total_by_vendor(self):
        vendor = Vendor.objects.get(user=request_object.user)
        subtotal = 0
        tax = 0
        tax_dict = {}

        if self.total_data:
            total_data = self.total_data
            data = total_data.get(str(vendor.id))

            for key, val in data.items():
                subtotal += float(key)

                if isinstance(val, str):
                    val = val.replace("'", '"')
                    val = json.loads(val)
                elif not isinstance(val, dict):
                    # Handle the case where val is neither a string nor a dictionary
                    continue
                
                tax_dict.update(val)
                # Calculate tax
                for tax_type, tax_rates in val.items():
                    for rate, amount in tax_rates.items():
                        tax += float(amount)

        total = float(subtotal) + float(tax)
        context = {
            'subtotal': subtotal,
            'tax_dict': tax_dict, 
            'total': total,
        }

        return context

    def __str__(self):
        return self.order_number
    
    
class OrderedItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.fooditem.food_title

    class Meta:
        verbose_name = "ordered items"
        verbose_name_plural = "ordered items"