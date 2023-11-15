from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import Vendor
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Q

def get_or_set_current_location(request):
    # if there is location in session
    # get lat and long from it
    if "lat" in request.session:
        lat = request.session.get('lat')
        long = request.session.get('long')
        return long,lat
    # if not, get them and also set in session storage
    elif "lat" in request.GET:
        lat = request.GET.get('lat')
        long = request.GET.get('lng')
        request.session['lat']=lat
        request.session['long']=long
        return long,lat
    else: return None


def home(request):
    # if there is long and lat
    if get_or_set_current_location(request):
        # set them 
        long,lat = get_or_set_current_location(request)
        # similar with search func
        pnt = GEOSGeometry('POINT(%s %s)'%(long,lat))
        vendors = Vendor.objects.filter(user_profile__location__distance_lte=(pnt,D(km=50))
                                        ).annotate(distance=Distance('user_profile__location',pnt)).order_by('distance')
        for v in vendors:
            v.kms = round(v.distance.km,1)

    else:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    # filter the approved and active vendor; limits the numver of display to 8
    context = {
        'vendors': vendors
    }
    # navigate also to user
    return render(request, 'home.html', context)