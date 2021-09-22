from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase


class CartTest(APITestCase):
    def setUp(self):
        self.payload_cart = {
            'product_id': 2
        }

    def test_add_item_empty_cart(self):
        url = reverse('add_to_cart')
        response = self.client.post(url, self.payload_cart, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_add_item_with_cart(self):
        cart = CartTest.test_add_item_empty_cart(self)
        url = reverse('add_to_cart')
        self.payload_cart['cart_id'] = cart['cart_id']
        self.payload_cart['product_id'] = 3
        response = self.client.post(url, self.payload_cart, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_add_item_with_product_quantity(self):
        url = reverse('add_to_cart')
        self.payload_cart['product_quantity'] = 1
        response = self.client.post(url, self.payload_cart, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_item_with_customer(self):
        url = reverse('add_to_cart')
        self.payload_cart['customer_id'] = 3
        response = self.client.post(url, self.payload_cart, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_clean_cart(self):
        cart = CartTest.test_add_item_empty_cart(self)
        url = reverse('cart', args=[cart['cart_id']])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_cart(self):
        cart = CartTest.test_add_item_empty_cart(self)
        url = reverse('cart', args=[cart['cart_id']])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_save_cart(self):
        cart = CartTest.test_add_item_with_customer(self)
        url = reverse('save_cart')
        self.payload_cart['cart_id'] = cart['cart_id']
        response = self.client.post(url, self.payload_cart, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return cart['customer_id']

    def test_retrieve_cart(self):
        customer_id = CartTest.test_save_cart(self)
        url = reverse('retrieve_cart', args=[customer_id])
        response = self.client.get(url, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ItemTest(APITestCase):
    def setUp(self):
        self.payload_cart = {
            'product_id': 2
        }

    def test_remove_item(self):
        cart = CartTest.test_add_item_empty_cart(self)
        url = reverse('remove_item')
        self.payload_cart['cart_id'] = cart['cart_id']
        self.payload_cart['product_id'] = cart['items'][0]['product_id']
        response = self.client.post(url, self.payload_cart, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_quantity_update(self):
        cart = CartTest.test_add_item_empty_cart(self)
        url = reverse('quantity_update')
        self.payload_cart['cart_id'] = cart['cart_id']
        self.payload_cart['product_quantity'] = 100
        response = self.client.put(url, self.payload_cart, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CouponTest(APITestCase):
    def setUp(self):
        self.payload_coupon = {
            'coupon_code': 'coupon_3'
        }
        self.payload_cart = {
            'product_id': 3
        }

    def test_add_coupon(self):
        cart = CartTest.test_add_item_empty_cart(self)
        url = reverse('coupon')
        self.payload_coupon['cart_id'] = cart['cart_id']
        response = self.client.post(url, self.payload_coupon, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_remove_coupon(self):
        cart = CouponTest.test_add_coupon(self)
        url = reverse('coupon')
        self.payload_coupon['cart_id'] = cart['cart_id']
        response = self.client.delete(url, self.payload_coupon, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)