from django.db import models
from Products.models import IceCream
from Users.models import User
import uuid
from django.utils import timezone
from django.core.signing import Signer
from datetime import timedelta
from itsdangerous import URLSafeSerializer
from django.conf import settings

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed','Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    owner = models.OneToOneField(User, verbose_name=("owner"), on_delete=models.CASCADE,related_name='order')
    order_status =models.CharField(max_length=20,choices=ORDER_STATUS_CHOICES,default='pending') 
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True,)
    
    def generate_signed_url(self):
        signer = URLSafeSerializer(settings.SECRET_KEY)
        expiration = (timezone.now() + timedelta(hours=1)).isoformat()
        signed_data = signer.dumps({'id': str(self.id), 'expiration': expiration})
        return f'{signed_data}'
    
    def delete_if_expired(self):
        expiration_date = self.created_at + timedelta(hours=24)
        if timezone.now() > expiration_date :
            self.delete()
              
    def __str__(self):
        return f"{self.owner.username} Order"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,verbose_name=("order"),on_delete=models.CASCADE,related_name="order_items")
    product = models.ForeignKey(IceCream, verbose_name=("icecream"),on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.order} Item"
    
