# Generated by Django 5.1.3 on 2024-11-20 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]