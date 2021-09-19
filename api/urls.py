from django.urls import path
from .views import add_to_cart, remove_item

urlpatterns = [
    path('add_to_cart', add_to_cart),
    path('remove_item', remove_item),
]
