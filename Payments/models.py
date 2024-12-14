from django.db import models
from Orders.models import Order
from itsdangerous import URLSafeSerializer
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
import uuid

# Create your models here.
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending','Pending'),
        ('failed','Failed'),
        ('completed','Completed'),
        ('refunded','Refunded'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('credit_card','Credit Card'),
        ('paypal','PayPal'),
        ('cash','Cash on Delivery'),
    ]
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    order = models.OneToOneField(Order, verbose_name=("order"),on_delete=models.CASCADE,related_name="payment")
    status = models.CharField( max_length=20 , choices=PAYMENT_STATUS_CHOICES)
    method = models.CharField(max_length=20,choices=PAYMENT_METHOD_CHOICES,)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=50,null=True,blank=True)
    
    def generate_signed_url(self):
        signer = URLSafeSerializer(settings.SECRET_KEY)
        expiration = (timezone.now() + timedelta(hours=1)).isoformat()
        signed_data = signer.dumps({'id': str(self.id), 'expiration': expiration})
        return f'{signed_data}'
        
    def __str__(self):
        return f"{self.order} Payment"