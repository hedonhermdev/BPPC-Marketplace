# Generated by Django 2.2.10 on 2020-05-24 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_merge_20200523_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='permission_level',
            field=models.SmallIntegerField(choices=[(0, 'Banned'), (1, 'Buyer'), (2, 'Seller'), (3, 'Admin')], default=2),
        ),
    ]
