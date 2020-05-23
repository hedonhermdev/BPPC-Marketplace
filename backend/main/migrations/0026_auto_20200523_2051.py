# Generated by Django 3.0.6 on 2020-05-23 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20200523_1825'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='productqna',
            options={'verbose_name': 'Product QnA', 'verbose_name_plural': 'Products QnA'},
        ),
        migrations.AlterField(
            model_name='product',
            name='expected_price',
            field=models.PositiveIntegerField(),
        ),
    ]
