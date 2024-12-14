from .models import Order
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
def send_order_confirmation_email(order):
    subject = "Order Confirmation - Sweet Scoop"
    message = (
        f"Dear {order.owner.username},\n\n"
        f"Thank you for placing your order with Sweet Scoop! We are excited to confirm your order:\n\n"
        f"Order ID: {order.id}\n\n"
        f"Here are the details of your order:\n"
        f"{display_order_items_names(order)}\n"
        f"Total Price: ${order.total_price}\n\n"
        "Your order is currently being processed, and we will notify you once it is ready for shipping. "
        "If you have any questions or need assistance, please do not hesitate to contact us.\n\n"
        "We sincerely appreciate your trust in us and look forward to serving you again soon!\n\n"
        "Best regards,\n"
        "The Sweet Scoop Team"
    )
    
    recipient_list= [order.owner.email]
    try:
        send_mail(
            subject=subject,
            message=message,
            recipient_list=recipient_list,
            from_email=settings.DEFAULT_FROM_EMAIL,
        )
    except Exception as e:
        messages.error(order.owner, f"Order confirmation email failed: {str(e)}")


def display_order_items_names(order):
    order_items_names = "".join(
        [
            f"- {item.product.name} (x{item.quantity}) - ${item.price}\n"
            for item in order.order_items.all()
        ]
    )
    return order_items_names