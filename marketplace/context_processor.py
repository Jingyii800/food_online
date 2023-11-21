from .models import Cart, Tax
from menu.models import FoodItem

def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)

# calculate the total price
def get_cart_amounts(request):
    subtotal = 0
    tax_dict = {}
    total = 0
    total_tax = 0
    if request.user.is_authenticated: # must login first
        cart_items = Cart.objects.filter(user=request.user)
        # calculate subtotal
        for item in cart_items:
            fooditem = FoodItem.objects.get(pk=item.fooditem.id)
            subtotal += fooditem.price * item.quantity

        get_tax = Tax.objects.filter(is_active=True)
        # calculate total tax
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round(subtotal*tax_percentage/100, 2)
            total_tax += tax_amount
            tax_dict.update({tax_type: {str(tax_percentage): tax_amount}})

        total = total_tax + subtotal # total amount
    return dict(total=total, subtotal=subtotal, tax=total_tax, tax_dict=tax_dict)