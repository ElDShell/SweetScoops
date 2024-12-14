from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from Orders.models import Order  

class Command(BaseCommand):
    help = 'Deletes orders that have been created more than 24 hours ago'

    def handle(self, *args, **kwargs):
        # Query for orders older than 24 hours
        expired_orders = Order.objects.filter(created_at__lt=timezone.now() - timedelta(hours=24))
        deleted_count, _ = expired_orders.delete()  # Delete the expired orders and get the count
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} expired orders"))
