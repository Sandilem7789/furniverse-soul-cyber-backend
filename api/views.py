# Imports
from django.http import JsonResponse
from django.contrib.auth.models import User         # For user authentication
from django.shortcuts import redirect


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer



# Auth View
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username,
        })

# Test Views
def hello_world(request):
    return JsonResponse({"message": "Hello, from furniverse backend!"})

def home(request):
    return redirect("http://localhost:5173")        # Redirect to frontend

# Featured Products
@api_view(['GET'])
def featured_products(request):
    products = Product.objects.filter(is_featured=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# ViewSets
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Product List
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# Categories List
def categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

# Register user
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    phone = request.data.get('phone')  # Optional for now

    if not username or not password or not email:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()

    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)