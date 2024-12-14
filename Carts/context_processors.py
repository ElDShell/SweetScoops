from .models import Cart
from django.core.exceptions import ObjectDoesNotExist

def cart_url_processor(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(owner=request.user)
            return  {'cart_url': cart.generate_signed_url()}
        except ObjectDoesNotExist:
            return {'cart_url':None}
    return {'cart_url':None}
