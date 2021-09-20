from django.urls import path
from .views import add_to_cart, remove_item, quantity_update, clean_cart, coupon

urlpatterns = [
    path('add_to_cart', add_to_cart),
    path('remove_item', remove_item),
    path('quantity_update', quantity_update),
    path('clean_cart', clean_cart),
    path('coupon', coupon),
]
