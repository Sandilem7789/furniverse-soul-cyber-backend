# Imports
from django.http import JsonResponse
from django.contrib.auth.models import User         # For user authentication
from django.shortcuts import redirect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

import hashlib
from urllib.parse import urlencode
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .models import (
    Product, Category, CartItem, 
    Order, OrderItem
    )

from .serializers import (
    ProductSerializer, CategorySerializer,
    CartItemSerializer, CartItemWriteSerializer,
    OrderSerializer, OrderItemSerializer,
)

from decouple import config

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
    return redirect(config("FRONTEND_URL", default="http://localhost:5173"))       # Redirect to frontend

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
    permission_classes = [AllowAny]  # Add appropriate permissions

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Product List
@api_view(['GET'])
@permission_classes([AllowAny])
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

# Cart Views
class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Add appropriate permissions
    
    def get_queryset(self):
        print("Cart request from:", self.request.user)
        return CartItem.objects.filter(user=self.request.user)

    
    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        user = self.request.user

        existing_item = CartItem.objects.filter(user=user, product=product).first()

        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
            print(f"Updated quantity for {product.name} to {existing_item.quantity}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer.save(user=user)
            print(f"New cart item created for {product.name} with quantity {quantity}")
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CartItemWriteSerializer  # handles incoming product ID
        return CartItemSerializer   # returns nested product info
    
    def destroy(self, request, *args, **kwargs):
        print("Deleting cart item:", kwargs.get("pk"))
        return super().destroy(request, *args, **kwargs)

# Order Views
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)


# PayFast Integration
def generate_payfast_url(order):
    from urllib.parse import urlencode
    import hashlib
    from decouple import config
    import logging

    logger = logging.getLogger(__name__)

    # Load secrets from env/config
    merchant_id = config("PAYFAST_MERCHANT_ID", default="10042860")
    merchant_key = config("PAYFAST_MERCHANT_KEY", default="bixilvur2t4k3")
    passphrase = config("PAYFAST_PASSPHRASE", default="")  # keep empty if none

    data = {
        "merchant_id": merchant_id,
        "merchant_key": merchant_key,
        "return_url": f"{config('FRONTEND_URL')}/order-confirmation/{order.id}",
        "cancel_url": f"{config('FRONTEND_URL')}/checkout",
        "notify_url": f"{config('BACKEND_URL')}/api/payfast/notify",
        "amount": "%.2f" % order.total,
        "item_name": f"Order #{order.id}",
        "m_payment_id": str(order.id),
    }

    # Signature string (exclude merchant_key)
    signature_keys = [
        "merchant_id",
        "return_url",
        "cancel_url",
        "notify_url",
        "amount",
        "item_name",
        "m_payment_id",
    ]

    signature_str = "&".join([f"{k}={data[k]}" for k in signature_keys if data.get(k)])
    if passphrase:
        signature_str += f"&passphrase={passphrase}"

    data["signature"] = hashlib.md5(signature_str.encode()).hexdigest()


    logger.debug("PayFast signature string: %s", signature_str)
    logger.debug("Generated signature: %s", data["signature"])

    base = "https://sandbox.payfast.co.za/eng/process?"
    redirect_url = base + urlencode(data)

    logger.debug("Final redirect URL: %s", redirect_url)
    return redirect_url




# PayFast Notify View
@csrf_exempt
def payfast_notify(request):
    if request.method == "POST":
        # Step 1: Extract POST data
        data = request.POST.dict()

        # Step 2: Verify signature (optional but recommended)
        signature_str = "&".join([f"{k}={v}" for k, v in data.items() if k != "signature"])
        signature_str += "&passphrase={passphrase}"
        expected_signature = hashlib.md5(signature_str.encode()).hexdigest()

        if data.get("signature") != expected_signature:
            return HttpResponse("Invalid signature", status=400)

        # Step 3: Update order status
        order_id = data.get("m_payment_id")
        payment_status = data.get("payment_status")

        # You can now mark the order as paid, failed, etc.
        # Example:
        # order = Order.objects.get(id=order_id)
        # order.status = "paid" if payment_status == "COMPLETE" else "failed"
        # order.save()

        return HttpResponse("ITN received", status=200)

    return HttpResponse("Invalid method", status=405)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_payfast_url(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    url = generate_payfast_url(order)
    print("Generated PayFast URL:", url)

    return Response({"url": url})
