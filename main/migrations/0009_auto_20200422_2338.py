# Generated by Django 2.2.10 on 2020-04-22 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20200422_1642'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='interested_buyers',
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='main.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
