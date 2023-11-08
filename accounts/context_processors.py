from vendor.models import Vendor


def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user = request.user)
    except: # when logout user is none, will not display error
        vendor = None
    return dict(vendor=vendor)