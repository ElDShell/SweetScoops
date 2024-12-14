from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import re
from itsdangerous import URLSafeSerializer
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
# Create your models here.

class User(AbstractUser):
    is_chef = models.BooleanField(default=False)
    address = models.CharField(max_length=255,null=True,blank=True)
    username =  models.CharField(max_length=150, unique=True)  # Ensures username is unique to use it as a slug in profile url
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_login = models.CharField( max_length=50,null=True,blank=True)
  
    def clean(self):
        super().clean()

        if self.first_name:
            if not re.match(r"^[a-zA-Z\s\-\'']+$", self.first_name):
                raise ValidationError('First name can only contain letters, spaces, hyphens, and apostrophes.')
            if len(self.first_name) > 20:
                raise ValidationError('First name cannot be longer than 20 characters.')

        
        if len(self.last_name) > 20:
            if not re.match(r"^[a-zA-Z\s\-\'']+$", self.last_name):
                raise ValidationError('Last name can only contain letters, spaces, hyphens, and apostrophes.')
            if len(self.last_name) > 20:
                raise ValidationError('Last name cannot be longer than 20 characters.')
        
    def genrate_signed_url(self):
        signer = URLSafeSerializer(settings.SECRET_KEY)
        expiration = (timezone.now() + timedelta(hours=1)).isoformat()
        signed_data = signer.dumps({'id': str(self.id), 'expiration': expiration})
        return f'{signed_data}'

        
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile") 
    image = models.ImageField(upload_to='img/profile',null=True,blank=True)
    phone_number = models.CharField(max_length=20,blank=True,null=True)
    role = models.CharField(max_length=20,default='Customer')
    # Only for chefs
    chef_bio = models.TextField(blank=True,null=True)
    chef_experince = models.PositiveIntegerField(blank=True,null=True)
    specialty = models.CharField(max_length=100,blank=True,null=True)
    slug = models.SlugField(unique=True,blank=True)
    # # social media link
    # fb_link = models.URLField(max_length=200,blank=True,null=True)
    # inst_link = models.URLField(max_length=200,blank=True,null=True)
    # twt_link = models.URLField(max_length=200,blank=True,null=True)
    
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)
    @staticmethod
    def create_profile(sender,instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)
        else:
            instance.profile.save()

@receiver(post_save,sender=User)
def create_or_update_profile(sender,instance,created,**kwargs):
    Profile.create_profile(sender,instance,created,**kwargs)

# class Delivery(models.Model):
#     DELIVERY_STATUS_CHOICES = [
#         ('pending','Pending'),
#         ('preparing','Preparing'),
#         ('out_for_delivery','Out for Delivery'),
#         ('delivered','Delivered'),
#         ('failed','Failed'),
#         ('cancelled','Cancelled'),
#     ]
#     order = models.ForeignKey(Order, verbose_name=("order"), on_delete=models.CASCADE)
#     delivery_address = models.CharField(max_length=50)
#     delivery_status = models.CharField(max_length=20, default="pending",choices=DELIVERY_STATUS_CHOICES)
#     deliverd_at = models.DateTimeField(blank=True,null=True)
#     def  __str__(self):
#         return f"Delivery Order for {self.order.owner.username}"

