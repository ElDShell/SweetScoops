# Generated by Django 5.1.3 on 2024-11-12 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(default='Customer', max_length=20),
        ),
    ]