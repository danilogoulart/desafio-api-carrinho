from django.urls import path
from .views import add_to_cart, remove_item, quantity_update, cart, coupon, save_cart, retrieve_cart

urlpatterns = [
    path('add_to_cart', add_to_cart, name="add_to_cart"),
    path('remove_item', remove_item, name="remove_item"),
    path('quantity_update', quantity_update, name="quantity_update"),
    path('cart/<uuid:pk>', cart, name="cart"),
    path('coupon', coupon, name="coupon"),
    path('save_cart', save_cart, name="save_cart"),
    path('retrieve_cart/<int:pk>', retrieve_cart, name="retrieve_cart")
]
