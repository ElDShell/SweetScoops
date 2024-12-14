from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import ListView,View
from .models import *
from Carts.models import *
from Carts.context_processors import cart_url_processor
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.middleware.csrf import get_token
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class ProductListView(ListView):
    model = IceCream
    template_name = "product.html"
    context_object_name = 'products'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_obj = paginator.get_page(self.request.GET.get('page'))
        
        context['is_paginated'] = page_obj.has_next()
        context['page_obj'] = page_obj  
        return context
    
    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            page = request.GET.get('page', 1)

            paginator = Paginator(self.get_queryset(), self.paginate_by)
            page_obj = paginator.get_page(page)
            csrf = get_token(request) 
            products_html = render_to_string('product_list_items.html', {'products': page_obj,'csrf_token': csrf})

            return JsonResponse({
                'products_html': products_html,
                'has_next': page_obj.has_next(),
                'page': page_obj.number
            })
        
        return super().get(request, *args, **kwargs)

class GalleryView(ListView):
    model = IceCream
    template_name = "gallery.html"
    context_object_name = "products"
    paginate_by = 6
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flavor = self.request.GET.get('flavor',None)
        if flavor:
            if flavor == "other":
                context["products"] = IceCream.objects.exclude(flavor__slug__in = ['fruit','vanilla','chocolate'] )    
            else :
                context["products"] = IceCream.objects.filter(flavor__slug =flavor)
        else:
            context['products'] = IceCream.objects.all()
        
        product_list = context['products']
        paginator = Paginator(product_list,6) 
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)
        
        context['flavor'] = flavor
        context['products'] = page
        
        print(f'flavor:{flavor}')
        return context
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            flavor = context.get('flavor', '')
            products = context['products']
            data = {
                'products':[
                    {
                        'id': product.id,
                        'name': product.name,
                        'img_url': product.img.url,
                        'price': product.price,
                    }
                    for product in products
                ],
                'flavor':flavor,
                'has_next':products.has_next(),
                'has_previous':products.has_previous(),
                'next_page_number':products.next_page_number() if products.has_next() else None,
                'previous_page_number':products.previous_page_number() if products.has_previous() else None,
            }
            return JsonResponse(data)
        return super().render_to_response(context, **response_kwargs)

class AddToCart(LoginRequiredMixin,View):
    
    def post(self, request):
        product_id = request.POST.get('product_id')
        product = get_object_or_404(IceCream,id=product_id)
        print(f'Product:{product}')
        
        cart, created = Cart.objects.get_or_create(owner=request.user)
        
        print(f'Cart:{cart}')

        cart_item = CartItem.objects.filter(cart=cart,product=product).first()
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            CartItem.objects.create(cart=cart,product=product,quantity=1,price=product.price)
        messages.success(request,f"{product.name} has been added yo your Cart")
        cart_url = cart_url_processor(request)['cart_url']
        print (f'CART:{cart_url}')
        return redirect('cart_detail',signed_data=cart_url)
            


    