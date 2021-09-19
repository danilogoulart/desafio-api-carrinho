import uuid
from django.utils import timezone
import json
from .mock import Product, Customer
from django.core.cache import cache
from rest_framework import serializers
from .models import Cart, CartItem
from django.db import models


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_quantity = serializers.IntegerField(required=False, default=1, min_value=0, max_value=10000)
    customer_id = serializers.IntegerField(required=False)
    cart_id = serializers.UUIDField(required=False)

    class Meta:
        fields = ['product_id', 'product_quantity', 'customer_id', 'cart_id']

    def validate_product(self, item):
        product = Product().get_product_by_id(item['product_id'])
        if product.get('message_error'):
            return product
        data = product
        data['product_quantity'] = item['product_quantity']
        if product['product_stock'] < 1:
            return {'message_error': 'The product is out of stock.'}
        if product['product_stock'] < item['product_quantity']:
            data['product_quantity'] = product['product_stock']
            data['message_warning'] = f'The product only has {product["product_stock"]} quantities in stock'
        data['total_item'] = product['product_price'] * data['product_quantity']

        return data

    def validate_customer(self, data):

        customer = {}
        if not data.get('customer_id'):
            customer['customer_id'] = customer['customer_name'] = customer['customer_email'] = customer[
                'customer_phone'] = customer['customer_gender'] = None
        else:
            cust = Customer().get_customer_by_id(data['customer_id'])

            if cust.get('message_warning'):
                return cust

            customer['customer_id'] = cust['customer_id']
            customer['customer_name'] = cust['customer_name']
            customer['customer_email'] = cust['customer_email']
            customer['customer_phone'] = cust['customer_phone']
            customer['customer_gender'] = cust['customer_gender']

        return customer

    def add_item(self, data, prod, customer):
        cart = {}
        cart = dict(cart, **customer)
        if not data.get('cart_id'):
            cart['cart_id'] = str(uuid.uuid4())
            prod['cart_id'] = cart['cart_id']
            cart['created_at'] = timezone.now()
            cart['updated_at'] = timezone.now()
            cart['coupon_id'] = cart['coupon_value'] = None
            cart['abandoned'] = False
            cart['items'] = [prod]
            cart = generate_totals(cart)
            save_cache(cart)
            return cart

        elif cache.get(data.get('cart_id')):

            cart = cache.get(data.get('cart_id'))
            product_in_cache = False
            for item in cart['items']:
                if prod['product_id'] == item['product_id']:
                    item['product_quantity'] += data['product_quantity']
                    if prod['product_stock'] < item['product_quantity']:
                        item['product_quantity'] = prod['product_stock']
                    item['total_item'] = item['product_quantity'] * item['product_price']
                    product_in_cache = True
            if not product_in_cache:
                if cart['items']:
                    cart['items'].append(prod)
                else:
                    cart['items'][0] = prod
            cart['updated_at'] = timezone.now()
            cart = generate_totals(cart)
            save_cache(cart)
            return cart


class RemoveItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    cart_id = serializers.UUIDField()

    class Meta:
        fields = ['product_id', 'cart_id']

    def remove_item(self, data):
        if cache.get(data.get('cart_id')):
            cart = cache.get(data.get('cart_id'))
            # return len(cart['items'])
            if len(cart['items']) == 1:
                if cart['items'][0]['product_id'] == data['product_id']:
                    cache.delete(data['cart_id'])
                    return {'message_success': 'Item removed successfully.', 'cart': None}
                else:
                    cart['message_warning'] = f'{data["product_id"]} not found'
                    return cart
            for item in cart['items']:
                if item['product_id'] == data['product_id']:
                    cart['items'].remove(item)
                    cart = generate_totals(cart)
                    save_cache(cart)
                    return cart
        else:
            return {'message_error': 'Cart not found.', 'cart': None}


def generate_totals(cart):
    subtotal = 0
    discount = 0
    for item in cart['items']:
        subtotal += item['total_item']
    if cart.get('coupon_value'):
        discount = cart['coupon_value']
    cart['total'] = subtotal - discount
    cart['subtotal'] = subtotal

    return cart


def save_cache(cart):
    cart['items'][0].pop('message_warning', None)
    cache.set(cart['cart_id'], cart, 60 * 60 * 24 * 5)
