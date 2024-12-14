from django.db import models
from Users.models import Profile
from django.core.exceptions import ValidationError
from Products.models import IceCream
# Create your models here.

class Review(models.Model):
    author = models.ForeignKey(Profile, verbose_name=("author"),on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField()

    def save(self,*args, **kwargs):
        if self.rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")
        return super().save(*args, **kwargs)
    def __str__(self):
        return f"Review:{self.author.user.username} on : {self.product.name}"
    