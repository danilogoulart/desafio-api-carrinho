from django.core.cache import cache
from django.db import models
from uuid import uuid4
import uuid
from django.utils import timezone
import json


class Cart(models.Model):
    cart_id = models.UUIDField(primary_key=True, null=False, blank=False, editable=False)
    total = models.PositiveIntegerField(blank=False, null=False)
    subtotal = models.PositiveIntegerField(blank=False, null=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    customer_id = models.PositiveIntegerField(null=True,blank=True)
    customer_name = models.CharField(max_length=255, null=True,blank=True)
    customer_email = models.CharField(max_length=255, null=True,blank=True)
    customer_phone = models.CharField(max_length=11, null=True,blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    customer_gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True,blank=True)
    coupon_id = models.PositiveIntegerField(null=True,blank=True)
    coupon_value = models.FloatField(null=True,blank=True)
    abandoned = models.BooleanField()


class CartItem(models.Model):
    cart_item_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product_id = models.PositiveIntegerField(blank=False, null=False)
    product_name = models.CharField(max_length=255, blank=False, null=False)
    product_sku = models.CharField(max_length=255, blank=False, null=False)
    product_img = models.URLField(max_length=255)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_price = models.FloatField(blank=False, null=False)
    product_quantity = models.PositiveIntegerField(blank=False, null=False)
    total_item = models.FloatField(blank=False, null=False)

