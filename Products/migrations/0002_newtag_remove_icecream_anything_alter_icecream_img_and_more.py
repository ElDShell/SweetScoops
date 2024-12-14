# Generated by Django 5.1.3 on 2024-11-13 08:13

import django.db.models.deletion
import taggit.managers
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='icecream',
            name='anything',
        ),
        migrations.AlterField(
            model_name='icecream',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='img/icecream'),
        ),
        migrations.CreateModel(
            name='UUIDTaggedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField(db_index=True, default=uuid.uuid4)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_tagged_items', to='contenttypes.contenttype', verbose_name='content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.newtag', verbose_name='uuid_tagged_items')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='icecream',
            name='flavor',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='Products.UUIDTaggedItem', to='Products.NewTag', verbose_name='flavors'),
        ),
    ]
