from django.db import models
import uuid
from Users.models import User
from Products.models import *
from django.core.signing import Signer
from django.utils import timezone
from datetime import timedelta
from itsdangerous import URLSafeSerializer
from django.conf import settings

class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    owner  = models.OneToOneField(User, verbose_name=("owner"),on_delete=models.CASCADE,related_name="cart")
    created_at = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def generate_signed_url(self):
        signer = URLSafeSerializer(settings.SECRET_KEY)
        expiration = (timezone.now() + timedelta(hours=1)).isoformat()
        signed_data = signer.dumps({'id': str(self.id), 'expiration': expiration})
        return f'{signed_data}'
    
    def total_price(self):
        if self.cart_items:
            return sum(item.price for item in self.cart_items.all())
        return 0
    
    def delete_if_expired(self):
        expiration_time = timezone.now() - timedelta(hours=24)
        if self.last_modified < expiration_time:
            self.delete()

    def __str__(self):
        return f"{self.owner.username} Cart"
    
class CartItem (models.Model):
    cart = models.ForeignKey(Cart, verbose_name=("cart"), on_delete=models.CASCADE,related_name='cart_items')
    product = models.ForeignKey(IceCream, verbose_name=("icecream"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    
    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.cart} Item"
         
    
    