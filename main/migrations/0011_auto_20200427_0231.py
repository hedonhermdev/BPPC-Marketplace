# Generated by Django 2.1.5 on 2020-04-26 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productbid',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='main.Product'),
        ),
    ]