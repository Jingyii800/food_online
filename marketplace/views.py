from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render,get_object_or_404
from .context_processor import get_cart_amounts, get_cart_counter
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from vendor.models import Vendor
from .models import Cart
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendors_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendors_count': vendors_count
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset= FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None    
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items
    }
    return render(request, 'marketplace/vendor_detail.html',context)

def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        # check if it's ajax request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check if the user already added that food to cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # increase cart quantity
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status': 'Success', 'message': "Added to cart", 
                                         'cart_count':get_cart_counter(request), 'qty': checkCart.quantity,
                                         'cart_amount': get_cart_amounts(request)})
                except:
                    # if not, create a new cart for user, quantity start from 1
                    checkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': "Added to cart", 
                                        'cart_count':get_cart_counter(request), 'qty': checkCart.quantity})

            except:
                return JsonResponse({'status': 'Failed', 'message': "This food item doesn't exist."})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request.'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue.'})
    
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        # check if it's ajax request:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if food item exists:
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check if there is food item already in carts
                try :
                    check_cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if check_cart.quantity>1:
                        # decrease the quantity
                        check_cart.quantity -= 1
                        check_cart.save()
                    else: # empty the cart
                        check_cart.delete()
                        check_cart.quantity=0
                    return JsonResponse({'status': 'Success', 'message': "Decreased 1 item.", 
                                         'qty':check_cart.quantity, 'cart_count': get_cart_counter(request),
                                         'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': "You do not have this item in the cart."})
            except:
                return JsonResponse({'status': 'Failed', 'message': "This food item doesn't exist."})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request.'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue.'})

@login_required(login_url='login')   
def cart(request):
    cartitmes = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cartitmes
    }
    return render(request, 'marketplace/cart.html', context)

@login_required(login_url='login')
def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if cart is exist
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': "This item is deleted from your cart", 
                                         'cart_count': get_cart_counter(request),'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This item does not exist in your cart'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request.'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue.'})
    
def search(request):
    if not 'address' in request.path:
        return redirect('marketplace')
    else:
        keyword = request.GET['keyword']
        address = request.GET['address']
        lat = request.GET['lat']
        long = request.GET['long']
        radius = request.GET['radius']
        # get vendor ids that has the food item the user is looking for
        fetch_vendors_by_food = FoodItem.objects.filter(food_title__icontains=keyword, 
                                                is_available=True).values_list('vendor', flat=True)
        # search vendors by ids or keyword in their names
        # vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_food) | 
        #                                 Q(vendor_name__icontains=keyword, is_approved=True, 
        #                                   user__is_active=True))
        if lat and long and radius:
            pnt = GEOSGeometry('POINT(%s %s)'%(long,lat))
            vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_food) | 
                                        Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True)
                                        , user_profile__location__distance_lte=(pnt, D(km=radius))
                                        ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")
        for v in vendors:
            # add a attri in vendor, that is v.km, distance is defined in annotate function
            v.kms = round(v.distance.km, 1)
        context = {
            'vendors':vendors,
            'source_location': address # take from request
        }
        return render(request, 'marketplace/listings.html', context)