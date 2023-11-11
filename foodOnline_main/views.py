from django.shortcuts import render
from django.http import HttpResponse

from vendor.models import Vendor

def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    # filter the approved and active vendor; limits the numver of display to 8
    context = {
        'vendors': vendors
    }
    # navigate also to user
    return render(request, 'home.html', context)