from django.urls import path, include
from . import views
from .views import (
    featured_products, 
    product_list, 
    categories, 
    CartItemViewSet
)

from .views import CustomAuthToken
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cart', CartItemViewSet, basename='cart')  # New cart endpoint

urlpatterns = [
    path('products/featured/', featured_products, name='featured_products'),
    path('products/', product_list, name='product_list'),
    path('categories/', categories, name='categories'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('register/', views.register_user, name='register'),  # New registration endpoint
]

urlpatterns += router.urls