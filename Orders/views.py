from django.shortcuts import render
from django.views.generic import TemplateView,View,DetailView
from .models import Order
from Payments.models import Payment
from django.shortcuts import redirect
from .utils import send_order_confirmation_email
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import get_object_from_signed_url

# Create your views here.
class OrderPaymentView(LoginRequiredMixin,TemplateView):
    template_name = "payment.html"
    
    def get_context_data(self, **kwargs): 
        context =  super().get_context_data(**kwargs)
        context['order'] = self.get_order()
        return context
    
    def get_order(self):
        order = get_object_from_signed_url(self.kwargs['signed_url'],Order)
        return order
    
    def get(self, request, *args, **kwargs):
        order = self.get_order()
        if order.owner != request.user:
            raise PermissionDenied('You are not allowed to see this page')
        return super().get(request, *args, **kwargs) 
    
    def post(self,request,*args, **kwargs):
        order = self.get_order()
        action = request.POST.get('action')
        order_signed_url = order.generate_signed_url()
        if action == "confirm":
            payment_method = request.POST.get('payment_method')
            
            if not payment_method:
                messages.error(request,"Payment Method is required")
                return redirect('order_payment',signed_url=order_signed_url)
            
            if payment_method == "paypal":
                return redirect('paypal_create',signed_url=order_signed_url)
            
            elif payment_method == "credit_card":
                messages.warning(request,"We will allow the Credit Card Soon please choose another method for now :(")
                return redirect ('order_payment',signed_url=order_signed_url)
            
            elif payment_method == "cash_on_delivery":
                order.order_status = "confirmed"
                order.save()
                order.delete() # for now
                messages.success(request,"Your Order has been confirmed for cash")
                return redirect('home')
            
            else:
                messages.error(request,"An expected error")
                return redirect('home')
        
        elif action == "cancel":
            order.order_status = 'cancelled'
            order.save()
            order.delete() # for now
            messages.info(request,"Your order has been cancelled")
            return redirect ('home')
        
        else :
            messages.error(request,"Invalid action. Please try again.")
            return redirect('home')



class OrderDetailView(LoginRequiredMixin,DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"
    
    def get_object(self, queryset = ...):
        order = get_object_from_signed_url(self.kwargs['signed_url'],Order)
        if self.request.user != order.owner:
            raise PermissionDenied('You are not allowed to see this page')
        return order

    def post(self,request,*args, **kwargs):
        action = request.POST.get('action')
        order = self.get_object()
        order_signed_url = order.generate_signed_url()
        if action == 'confirm':
            if order.order_status == 'pending':
                order.order_status= 'confirmed'
                order.save()
                order_payment = Payment.objects.filter(order=order).first()
                if not order_payment: 
                    send_order_confirmation_email(order)
                    messages.success(request,"Your order has been confirmed")
                    return redirect('order_payment',signed_url=order_signed_url)
                else :
                    messages.error(request,"There is a Payment for this order Check it out...")
                    return redirect('order_payment',signed_url=order_signed_url)
            else :
                messages.warning(request,"This order cannot be confirmed")
        elif action == 'cancel':
            if order.order_status == 'pending':
                order.order_status = 'cancelled'
                messages.info(request,"Your Order has been Cancelled")
                order.save()
                order.delete() # for now
                return redirect('home')
            else:
                messages.warning(request,"This order cannot be cancelled")
        elif action == 'delete':
            order.delete()
            return redirect('home')
        messages.error(request,"Something went wrong, Please try again later...")
        return redirect('home')

            
            
