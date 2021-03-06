from django.core.cache import cache
from django.db import models
from uuid import uuid4
import uuid
from django.utils import timezone
import json


class Cart(models.Model):
    cart_id = models.UUIDField(primary_key=True, null=False, blank=False, editable=False)
    total = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    customer_id = models.PositiveIntegerField(null=True,blank=True)
    customer_name = models.CharField(max_length=255, null=True,blank=True)
    customer_email = models.CharField(max_length=255, null=True,blank=True)
    customer_phone = models.CharField(max_length=11, null=True,blank=True)
    customer_gender = models.CharField(max_length=1, null=True, blank=True)
    coupon_id = models.PositiveIntegerField(null=True,blank=True)
    coupon_code = models.CharField(max_length=100, null=True, blank=True)
    coupon_percentage_value = models.PositiveIntegerField(null=True, blank=True)


class CartItem(models.Model):
    cart_item_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product_id = models.PositiveIntegerField(blank=False, null=False)
    product_name = models.CharField(max_length=255, blank=False, null=False)
    product_sku = models.CharField(max_length=255, blank=False, null=False)
    product_active = models.BooleanField(blank=False, null=False)
    product_img = models.URLField(max_length=255)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_price = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False)
    product_quantity = models.PositiveIntegerField(blank=False, null=False)
    total_item = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False)

