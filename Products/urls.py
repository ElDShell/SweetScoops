from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('gallery/',GalleryView.as_view(),name='gallery'),
    path('add/', AddToCart.as_view(), name='add_to_cart'),
    
]
