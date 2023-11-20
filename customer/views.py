from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.forms import UserInfoForm, UserProfileForm
from accounts.models import User, UserProfile
from accounts.views import check_role_customer
from django.contrib import messages
import simplejson as json
from orders.models import Order, OrderedItems

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def c_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method=='POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        userinfo_form = UserInfoForm(request.POST, instance=request.user)
        if profile_form.is_valid() and userinfo_form.is_valid():
            userinfo_form.save()
            profile_form.save()
            messages.success(request, "Your profile updated successfully!")
            return redirect('c_profile')
        else:
            print(profile_form.errors)
            print(userinfo_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        userinfo_form = UserInfoForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'userinfo': userinfo_form,
        'profile': profile,

    }
    return render(request, 'customer/c_profile.html', context)


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'customer/my_orders.html', context)


def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
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
    except:
        return redirect('customer')
    return render(request, 'customer/order_detail.html',context)