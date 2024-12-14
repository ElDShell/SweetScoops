from Orders.models import Order,OrderItem
from itsdangerous import URLSafeSerializer
from django.conf import settings
from django.utils import timezone
from django.http import Http404
from Users.models import User
from itsdangerous import BadSignature 
from django.db import transaction
from django.core.exceptions import ValidationError

def create_order(cart):
    if not cart.cart_items.exists():
        return None

    try:
        with transaction.atomic():
            order = Order.objects.create(
                owner=cart.owner,
                total_price=cart.total_price()
            )

            for cart_item in cart.cart_items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price * cart_item.quantity,
                )

            cart.cart_items.all().delete()
            cart.delete()
            return order

    except ValidationError as e:
        print(f"Error creating order: {e}")
        return None
     
def get_object_from_signed_url(signed_url,obj_class):
    signer = URLSafeSerializer(settings.SECRET_KEY)
    try:
        signed_data = signer.loads(signed_url)
        obj_id = signed_data['id']
        expiration = signed_data['expiration']
        
        expiration_time = timezone.datetime.fromisoformat(expiration)
        if timezone.now() > expiration_time:
            raise Http404 ('This link has been expired!!!')
        if not hasattr(obj_class,'objects'):
            raise ValueError(f"This {obj_class} class is not a model")

        obj = obj_class.objects.get(id=obj_id)
        return obj
    except (BadSignature,KeyError,):
        raise Http404("Invalid or expired link")
    except ValueError:
        raise Http404('Invalid class')
    except obj_class.DoesNotExist:
        raise Http404("There is no object match these data")
