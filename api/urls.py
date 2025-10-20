from django.urls import path, include
from . import views
from .views import (
    featured_products, 
    product_list, 
    categories, 
    CartItemViewSet,
    OrderViewSet,
    OrderItemViewSet,
    payfast_notify,
)
from .views import get_payfast_url

from .views import CustomAuthToken
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cart', CartItemViewSet, basename='cart')                                  # cart endpoint
router.register(r'orders', OrderViewSet, basename='orders')                                 # orders endpoint
router.register(r'order-items', OrderItemViewSet, basename='order-items')                   # order items endpoint

urlpatterns = [
    path('products/featured/', featured_products, name='featured_products'),
    path('products/', product_list, name='product_list'),
    path('categories/', categories, name='categories'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('register/', views.register_user, name='register'),                                # registration endpoint
    path("payfast/notify", payfast_notify, name="payfast-notify"),                          # PayFast notify endpoint
]

urlpatterns += router.urls
urlpatterns += [
    path("payfast-url/<int:order_id>/", get_payfast_url, name="payfast-url"),
]