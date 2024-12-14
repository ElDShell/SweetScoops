from django.urls import path
from .views import *
urlpatterns = [
    path('cart/<str:signed_data>/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/item/remove/',RemoveFromCart.as_view(),name='cart_item_remove'),
    path('cart/item/update/',CartItemUpdateView.as_view(),name='cart_item_update'),
    path('cart/to/order/', CartToOrder.as_view(), name="cart_to_order")
]
