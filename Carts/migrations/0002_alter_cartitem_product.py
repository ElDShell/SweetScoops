# Generated by Django 5.1.3 on 2024-11-11 12:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Carts', '0001_initial'),
        ('Products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.icecream', verbose_name='icecream'),
        ),
    ]
