from django.urls import path, include
from . import views
from .views import featured_products, product_list, categories

urlpatterns = [
    path("hello/", views.hello_world, name="hello_world"),
    path('products/featured/', featured_products, name='featured_products'),
    path('products/', product_list, name='product_list'),
    path('categories/', categories, name='categories'),
    path('api/', include('router.urls')),   
]