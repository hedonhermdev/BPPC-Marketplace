# Generated by Django 2.2.10 on 2020-05-25 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20200524_2248'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='created',
            new_name='created_at',
        ),
    ]