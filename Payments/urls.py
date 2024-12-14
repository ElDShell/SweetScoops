from django.urls import path
from .views import *

urlpatterns = [
    path("paypal/payment/create/<str:signed_url>", PaypalPaymentCreateView.as_view(), name="paypal_create"),
    path("payment/success/", PaypalPaymentSuccessView.as_view(), name="payment_success"),
    path("payment/cancel/", PaypalPaymentCancelView.as_view(), name="payment_cancel"),
]
