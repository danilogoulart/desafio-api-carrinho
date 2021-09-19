from rest_framework.decorators import api_view
from .serializers import AddToCartSerializer
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
