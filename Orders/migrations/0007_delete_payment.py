# Generated by Django 5.1.3 on 2024-11-30 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0006_alter_orderitem_order_alter_payment_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
