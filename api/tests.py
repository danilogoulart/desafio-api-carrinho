from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase


class CartTest(APITestCase):
    def setUp(self):
        self.payload = {
                'product_id': 2
            }

    def test_add_item_empty_cart(self):
        url = reverse('add_to_cart')
        response = self.client.post(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_add_item_with_cart(self):
        cart = CartTest.test_add_item_empty_cart(self)
        url = reverse('add_to_cart')
        self.payload['cart_id'] = cart['cart_id']
        self.payload['product_id'] = 3
        response = self.client.post(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_add_item_with_product_quantity(self):
        url = reverse('add_to_cart')
        self.payload['product_quantity'] = 1
        response = self.client.post(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_clean_cart(self):
        cart = CartTest.test_add_item_empty_cart(self)
        url = reverse('cart', args=[cart['cart_id']])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    
class RemoveItemTest(APITestCase):
    def setUp(self):
        self.payload = {
            'product_id': 2
        }

    def test_remove_item(self):
        cart = CartTest.test_add_item_empty_cart(self)
        url = reverse('remove_item')
        self.payload['cart_id'] = cart['cart_id']
        self.payload['product_id'] = cart['items'][0]['product_id']
        response = self.client.post(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data
