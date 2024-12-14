from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.views.generic import View
from Orders.models import Order
from .models import Payment
from django.urls import reverse_lazy
from utils import get_object_from_signed_url
from django.contrib import messages
from django.core.exceptions import PermissionDenied
import paypalrestsdk
from django.contrib.auth.mixins import LoginRequiredMixin

 
paypalrestsdk.configure({
    "mode":settings.PAYPAL_MODE,
    "client_id":settings.PAYPAL_CLIENT_ID,
    "client_secret":settings.PAYPAL_CLIENT_SECRET ,
}) 
class PaypalPaymentCreateView(LoginRequiredMixin,View):
    def get(self,request,signed_url):
        try:
            order = get_object_from_signed_url(signed_url,Order)
            if request.user != order.owner:
                raise PermissionDenied("You are not allowed to see this")
            
            paypal_payment = paypalrestsdk.Payment({
                "intent":"sale",
                "payer":{
                    "payment_method":"paypal"
                },
                "redirect_urls":{
                    "return_url": request.build_absolute_uri(reverse_lazy('payment_success')),
                    "cancel_url": request.build_absolute_uri(reverse_lazy('payment_cancel'))
                },
                "transactions":[{
                    "amount":{
                        "total":f"{order.total_price:.2f}",
                        "currency":"USD"
                    },
                    "description":f"Payment for order {order.id}"
                }],   
            })
            
            if paypal_payment.create():
                Payment.objects.create(
                    order=order,
                    transaction_id=paypal_payment.id,
                    amount=order.total_price,
                    method="paypal",
                    status="pending",
                )
                for link in paypal_payment.links:
                    print(f"Link: {link.rel}, URL: {link.href}")

                    if link.rel == "approval_url":
                        return redirect(link.href)
                messages.error(request,"No approval url found")
                return redirect("order_payment",signed_url=order.generate_signed_url())
            else:
                print("PayPal Payment Error:", paypal_payment.error)
                messages.error(request,"Failed to create paypal payment")
                return redirect("order_payment",signed_url=order.generate_signed_url())
        except Http404:
            raise
        except Exception as e: 
            messages.error(request,f"un expected Error occured {str(e)}")
            return redirect("order_payment",signed_url=order.generate_signed_url())
 
class PaypalPaymentSuccessView(LoginRequiredMixin,View):
    def get(self,request):
        payment_id = request.GET.get('paymentId')
        payer_id= request.GET.get('PayerID')
        
        try:
            paypal_payment = paypalrestsdk.Payment.find(payment_id)
            if paypal_payment.execute({"payer_id":payer_id}):
                payment = Payment.objects.get(transaction_id=payment_id)
                payment.status = 'completed'
                payment.save()
                
                order = payment.order
                order.order_status = "confirmed"
                order.save()
                
                messages.success(request,"Payment sccessfully")
                order.delete() # for now
                return redirect('home')
            else:
                messages.error(request,"Payment failed during execution.")
                return redirect("order_payment",signed_url=order.generate_signed_url())
            
        except Payment.DoesNotExist:
            messages.error(request,"Payment not found")
            return redirect('home')
        
        except Exception as e:
            messages.error(request,f"Something went wrong {e}")
            return redirect('home')
        
class PaypalPaymentCancelView(LoginRequiredMixin,View):
    def get(self,request):
        messages.info(request,"Payment Was canceled.")
        return redirect('home')            
 
        
        