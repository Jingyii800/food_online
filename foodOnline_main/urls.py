from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)