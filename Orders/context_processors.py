from .models import Order
from django.core.exceptions import  ObjectDoesNotExist

def order_url_processor(request):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(owner=request.user)
            return {'order_url':order.generate_signed_url()}
        except ObjectDoesNotExist:
            return {'order_url':None}
    return {'order_url':None}
