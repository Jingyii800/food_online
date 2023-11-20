from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from accounts.utils import send_notification
from marketplace.context_processor import get_cart_amounts
from marketplace.models import Cart
from orders.forms import OrderForm
from orders.models import Order, OrderedItems, Payment
import simplejson as json
from django.contrib.auth.decorators import login_required
from orders.utils import generate_order_number

@login_required(login_url='login')
def place_order(request):
    # check cart is not empty
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')

    # place order
    total_tax = get_cart_amounts(request)['tax']
    total = get_cart_amounts(request)['total']
    tax_data = get_cart_amounts(request)['tax_dict']
    # create the order object
    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.zip_code = form.cleaned_data['zip_code']
            order.user = request.user
            order.total = total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save()
            order.order_number = generate_order_number(order.id)
            order.save()
            # after created, move to the confirm page
            context = {
                'order': order,
                'cart_items': cart_items,
            }
            return render(request,'orders/place_order.html', context)
        else:
            print(form.errors)

@login_required(login_url='login')
def payments(request):
    # if request is ajax
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == 'POST':
    # store payment details
            # create payment object
            payment = Payment(
                user = request.user,
                transaction_id = request.POST.get('transaction_id'),
                payment_method = request.POST.get('payment_method'),
                amount = request.POST.get('amount'),
                status = request.POST.get('status')
            )
            payment.save()
    # update order model
            order_number = request.POST.get('order_number')
            order = Order.objects.get(user=request.user, order_number=order_number)
            order.payment = payment
            order.is_ordered = True
            order.save()
    # move cartitems to ordered model
            cart_items = Cart.objects.filter(user=request.user)
            for item in cart_items:
                ordered_food = OrderedItems(
                    order = order,
                    payment = payment,
                    user = request.user,
                    fooditem = item.fooditem,
                    quantity = item.quantity,
                    price = item.fooditem.price,
                    amount = item.quantity * item.fooditem.price # total amount
                )
                ordered_food.save()
    # send order confirmation email to customer
            mail_subject = "Thanks for ordering with us."
            mail_template = 'orders/order_confirmation.html'
            context = {
                'user': order.user,
                'order': order,
                'to_email': order.email
            }
            send_notification(mail_subject, mail_template, context)
    # send order recieve email to vendor
            mail_subject = "You have received a new order."
            mail_template = 'orders/order_vendor_received.html'
            to_emails = []
            # loop to send emails to all vendors in this order
            for i in cart_items:
                if i.fooditem.vendor.user.email not in to_emails:
                    to_emails.append(i.fooditem.vendor.user.email)
            context = {
                'order': order,
                'to_email': to_emails
            }            
            send_notification(mail_subject, mail_template, context)
    # clean the cart
            # cart_items.delete()
    # return back to ajax when status is success
            response = {
                'order_number': order_number,
                'transaction_id': payment.transaction_id,
            }
            return JsonResponse(response)
    # return back to ajax when status is failed
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request.'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue.'})

def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')
    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id = transaction_id, is_ordered=True)
        ordered_food = OrderedItems.objects.filter(order=order)
        subtotal = 0
        for i in ordered_food:
            subtotal += i.quantity * i.price
        # load tax_data in json format
        tax_data = json.loads(order.tax_data)
        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': subtotal,
            'tax_data': tax_data
        }
        return render(request, 'orders/order_complete.html',context )
    except:
        return redirect('home')
