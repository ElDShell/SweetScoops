import uuid
from django.db import models
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase,TagBase
# Create your models here.

class NewTag(TagBase):
    pass
class UUIDTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(NewTag ,verbose_name=("uuid_tagged_items"), on_delete=models.CASCADE)
    object_id = models.UUIDField(db_index=True,default=uuid.uuid4)

class IceCream(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=50)
    flavor = TaggableManager(through=UUIDTaggedItem,verbose_name="flavors",blank=True)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    description = models.TextField()
    img = models.ImageField(
        upload_to='img/icecream', height_field=None, width_field=None, max_length=None,null=True,blank=True
    )
    created_by = models.CharField(max_length=50,default="SweetScoops")
    def __str__(self):
        return f"IceCream:{self.name}"

    