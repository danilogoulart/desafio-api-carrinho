import uuid
from django.utils import timezone
from .mock import Product, Customer, Coupon
from django.core.cache import cache
from rest_framework import serializers
from .models import Cart, CartItem



class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_quantity = serializers.IntegerField(required=False, default=1, min_value=1, max_value=10000)
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
            cart['coupon_id'] = cart['coupon_percentage_value'] = None
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
            prod['cart_id'] = cart['cart_id']
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
            if len(cart['items']) == 1:
                if cart['items'][0]['product_id'] == data['product_id']:
                    cache.delete(data['cart_id'])
                    return {'message_success': 'Item removed successfully.', 'cart': None}
                else:
                    cart['message_warning'] = f'product_id: {data["product_id"]} not found'
                    return cart
            for item in cart['items']:
                if item['product_id'] == data['product_id']:
                    cart['items'].remove(item)
                    cart = generate_totals(cart)
                    save_cache(cart)
                    return cart
        else:
            return {'message_error': 'Cart not found.', 'cart': None}


class QuantityUpdateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    cart_id = serializers.UUIDField()
    product_quantity = serializers.IntegerField(min_value=1, max_value=10000)

    class Meta:
        fields = ['product_id', 'cart_id', 'product_quantity']

    def quantity_update(self, data):
        if cache.get(data.get('cart_id')):
            cart = cache.get(data.get('cart_id'))
            for item in cart['items']:
                if item['product_id'] == data['product_id']:
                    item['product_quantity'] = data['product_quantity']
                    if item['product_stock'] < data['product_quantity']:
                        item['product_quantity'] = item['product_stock']
                    item['total_item'] = item['product_quantity'] * item['product_price']
                    cart = generate_totals(cart)
                    save_cache(cart)
                    return cart
            cart['message_warning'] = f'product_id: {data["product_id"]} not found'
            return cart
        else:
            return {'message_error': 'Cart not found.', 'cart': None}

class CleanCartSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    class Meta:
        fields = ['cart_id']

    def clean_cart(self, data):
        if cache.get(data.get('cart_id')):
            cache.delete(data['cart_id'])
            return {'message_success': 'Cart successfully deleted'}
        else:
            return {'message_error': 'Cart not found.', 'cart': None}


class AddCouponSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    coupon_code = serializers.CharField()

    class Meta:
        fields = ['cart_id', 'coupon_code']

    def add_coupon(self, data):
        if cache.get(data.get('cart_id')):
            cart = cache.get(data['cart_id'])
            if cart['coupon_id']:
                return {'message_error': 'Cart already has a discount coupon.'}
            coupon = Coupon().get_coupons_by_code(data['coupon_code'])
            if coupon.get('message_error'):
                return coupon
            cart['coupon_id'] = coupon['coupon_id']
            cart['coupon_percentage_value'] = coupon['coupon_percentage_value']
            cart['coupon_code'] = coupon['coupon_code']
            cart = generate_totals(cart)
            save_cache(cart)
            return cart
        else:
            return {'message_error': 'Cart not found.', 'cart': None}


class RemoveCouponSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    class Meta:
        fields = ['cart_id', 'coupon_code']

    def remove_coupon(self, data):
        if cache.get(data.get('cart_id')):
            cart = cache.get(data['cart_id'])
            cart['coupon_id'] = None
            cart['coupon_percentage_value'] = None
            cart['coupon_code'] = None
            cart = generate_totals(cart)
            save_cache(cart)
            return cart
        else:
            return {'message_error': 'Cart not found.', 'cart': None}

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        Model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    cart_id = serializers.UUIDField()

    class Meta:
        model = Cart
        fields = ['cart_id']

    def create(self, data):
        if cache.get(data['cart_id']):
            cart = cache.get(data['cart_id'])
            items = cart.pop('items')
            Cart.objects.create(**cart)
            for item in items:
                CartItem.objects.create(**item)
            cache.delete(data['cart_id'])
            return {"message_success": "Cart successfully persisted."}

def generate_totals(cart):
    subtotal = discount = 0
    for item in cart['items']:
        subtotal += item['total_item']
    if cart.get('coupon_percentage_value'):
        discount = cart['coupon_percentage_value']
    cart['total'] = subtotal - (subtotal * discount/100)
    cart['subtotal'] = subtotal
    return cart


def save_cache(cart):
    cart['items'][0].pop('message_warning', None)
    cache.set(cart['cart_id'], cart, 60 * 60 * 24 * 5)