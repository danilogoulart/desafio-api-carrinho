from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from .models import Cart
from .serializers import AddToCartSerializer, RemoveItemSerializer, QuantityUpdateSerializer, AddCouponSerializer, RemoveCouponSerializer, CartSerializer, RetrieveCartSerializer
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def add_to_cart(request):
    if request.method == 'POST':
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.validate_customer(serializer.data)

            serializer = serializer.add_item(serializer.data, customer)

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


@api_view(['DELETE', 'GET'])
def cart(request, pk):
    request.data['cart_id'] = pk
    serializer = CartSerializer(data=request.data)
    if serializer.is_valid():
        if request.method == 'DELETE':
            serializer = serializer.clean_cart(request.data)
            if serializer.get('message_error'):
                return Response(serializer, status.HTTP_400_BAD_REQUEST)
            return Response(serializer, status=status.HTTP_200_OK)
        if request.method == 'GET':
            serializer = serializer.get_cart_by_id(request.data)
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
                return Response(serializer, status.HTTP_404_NOT_FOUND)
            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        serializer = RemoveCouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.remove_coupon(serializer.data)
            if serializer.get('message_error'):
                return Response(serializer, status.HTTP_404_NOT_FOUND)
            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def retrieve_cart(request, pk):
    if request.method == 'GET':
        try:
            serializer = RetrieveCartSerializer(Cart.objects.filter(customer_id=pk).latest('created_at'))
            serializer = serializer.validate_cart(serializer.data)
            return Response(serializer, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("Cart not found.", status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def save_cart(request):
    if request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.create(serializer.data)
            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
