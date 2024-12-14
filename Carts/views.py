from django.views.generic import View,DetailView
from django.contrib import messages
from .models import *
from .context_processors import cart_url_processor
from django.http import Http404,JsonResponse
from django.shortcuts import get_object_or_404,redirect
from django.core.signing import Signer,BadSignature
from django.utils import timezone
from itsdangerous import URLSafeSerializer , BadSignature
from utils import create_order
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class CartDetailView(LoginRequiredMixin,DetailView):
    model = Cart
    template_name = "cart.html"
    context_object_name = 'cart'
    
    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        if not cart.cart_items.exists():
            messages.error(request,"Your cart is empty, Please add items to proceed.")
            return redirect('home')
        return super().get(request, *args, **kwargs)
    
    def get_object(self):
        signed_data = self.kwargs['signed_data']
        signer = URLSafeSerializer(settings.SECRET_KEY)
        
        try:
            data = signer.loads(signed_data)
            cart_id= data['id']
            expiration = timezone.datetime.fromisoformat(data['expiration'])
            
            if timezone.now() > expiration:
                raise Http404('This link has expired')
            
            cart =  get_object_or_404(Cart,id=cart_id)
            
        except (ValueError,Cart.DoesNotExist,BadSignature):
            raise Http404('Invalid or expired link')
        if self.request.user != cart.owner:
            raise PermissionDenied('You are not allowed to see this page')

        return cart

class RemoveFromCart(LoginRequiredMixin,View):
    def post(self, request):
        cart_item_id = request.POST.get('delete_cart_item')
        print(cart_item_id)
        if cart_item_id:
            try:
                cart_item = CartItem.objects.get(id=cart_item_id)
                
                cart_item.delete()

                messages.info(request, f"{cart_item.product.name} removed successfully!")  
            except CartItem.DoesNotExist:
                messages.error(request, "Cart item not found.")
                return redirect('cart')  
        else:
            messages.error(request, "No product specified to remove.")
        cart_url = cart_url_processor(request)['cart_url']
        return redirect('cart_detail',signed_data=cart_url) 

class CartItemUpdateView(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        
        try:
            cart_item = CartItem.objects.get(id=item_id)
            
            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1

            cart_item.save()
            print(f'Total:{cart_item.cart.total_price()}')
            return JsonResponse({
                'success':True,
                'new_quantity':cart_item.quantity,
                'new_price':cart_item.price,
                'new_total_price':cart_item.cart.total_price(),
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart item not found'})

class CartToOrder(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        cart_id = request.POST.get('cart_id')
        cart = get_object_or_404(Cart,id=cart_id)
        
        if hasattr(request.user,'order'):
            messages.info(request,"Please finish the current order before making new one")
            return redirect('order_detail',signed_url=request.user.order.generate_signed_url())
            
        if not cart.cart_items.exists():
            messages.error(request,'the cart is empty, Cannot create the order')
            return redirect('cart_detail',signed_url=cart.generate_signed_url())
        
        order = create_order(cart)
        
        if order:
            return redirect ('order_detail',signed_url=order.generate_signed_url())
        
        else:
            messages.error(request,'There was an error of creating the order, please try again later')
            return redirect('cart_detail',signed_url=cart.generate_signed_url())
        
        
        