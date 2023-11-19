from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.urls import include
from marketplace import views as MarketplaceViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('accounts.urls')),
    path('marketplace/', include('marketplace.urls')),

    # search path
    path('search/', MarketplaceViews.search, name='search'),

    # checkout page
    path('checkout/', MarketplaceViews.checkout, name='checkout'),

    # order path
    path('orders/', include('orders.urls'))
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
