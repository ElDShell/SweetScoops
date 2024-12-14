from django.urls import path
from .views import *


urlpatterns = [
    path('order/payment/<str:signed_url>',OrderPaymentView.as_view(),name='order_payment'),    
    path('order/<str:signed_url>/', OrderDetailView.as_view(), name='order_detail')
]
