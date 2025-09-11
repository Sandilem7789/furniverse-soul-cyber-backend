from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from api.views import home
from rest_framework.routers import DefaultRouter
from api.views import ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path("", home),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),     # DRF viewsets
    path('api/', include('api.urls')),      # Custom views like login
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
