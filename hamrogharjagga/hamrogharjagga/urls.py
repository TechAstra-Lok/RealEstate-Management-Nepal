from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home.api import api_properties, api_submit_inquiry, api_live_stats

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('seller/', include('seller.urls')), 
    path('buyer/', include('buyer.urls')),   
    
    # Asynchronous / Real-time JSON API endpoints
    path('api/properties/', api_properties, name='api_properties'),
    path('api/inquiries/', api_submit_inquiry, name='api_submit_inquiry'),
    path('api/stats/', api_live_stats, name='api_live_stats'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
