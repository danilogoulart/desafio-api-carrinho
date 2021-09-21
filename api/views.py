from django.core.cache import cache
from rest_framework.decorators import api_view
from .serializers import AddToCartSerializer, RemoveItemSerializer, QuantityUpdateSerializer, CleanCartSerializer, AddCouponSerializer, RemoveCouponSerializer, CartSerializer
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def add_to_cart(request):
    if request.method == 'POST':
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validate_product(serializer.data)
            if product.get('message_error'):
                return Response(product, status.HTTP_400_BAD_REQUEST)

            customer = serializer.validate_customer(serializer.data)

            serializer = serializer.add_item(serializer.data, product, customer)

            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def remove_item(request):
    if request.method == 'POST':
        serializer = RemoveItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.remove_item(serializer.data)
            if serializer.get('message_error'):
                return Response(serializer, status.HTTP_400_BAD_REQUEST)
            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def quantity_update(request):
    if request.method == 'PUT':
        serializer = QuantityUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.quantity_update(serializer.data)
            if serializer.get('message_error'):
                return Response(serializer, status.HTTP_400_BAD_REQUEST)
            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def clean_cart(request):
    if request.method == 'DELETE':
        serializer = CleanCartSerializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.clean_cart(serializer.data)
            if serializer.get('message_error'):
                return Response(serializer, status.HTTP_400_BAD_REQUEST)
            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'DELETE'])
def coupon(request):
    if request.method == 'POST':
        serializer = AddCouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.add_coupon(serializer.data)
            if serializer.get('message_error'):
                return Response(serializer, status.HTTP_400_BAD_REQUEST)
            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        serializer = RemoveCouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.remove_coupon(serializer.data)
            if serializer.get('message_error'):
                return Response(serializer, status.HTTP_400_BAD_REQUEST)
            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def save_cart(request):
    if request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.create(serializer.data)
            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)