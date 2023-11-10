from foodOnline_main import settings
from vendor.models import Vendor


def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user = request.user)
    except: # when logout user is none, will not display error
        vendor = None
    return dict(vendor=vendor)

def get_googleApi(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}