from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import Product, Category

from .serializers import ProductSerializer, CategorySerializer

def hello_world(request):
    return JsonResponse({"message": "Hello, from furniverse backend!"})     # Simple test endpoint

def home(request):
    return JsonResponse({"message": "Welcome to the Furniverse API!"})      # Home test endpoint

@api_view(['GET'])
def featured_products(request):
    products = Product.objects.filter(is_featured=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        respone = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username
        })