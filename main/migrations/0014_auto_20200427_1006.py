# Generated by Django 2.1.5 on 2020-04-27 04:36

from django.db import migrations
from ..models import CATEGORY_CHOICES, Category

def create_category_choices(apps, schema_editor):
    for choice in CATEGORY_CHOICES:
        Category.objects.create(name=choice)

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20200427_0313'),
    ]

    operations = [
        migrations.RunPython(create_category_choices)
    ]