# Generated by Django 2.2.10 on 2020-05-08 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20200502_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.CharField(choices=[('default', 'default_avatar.png'), ('male1', 'male_avatar.png'), ('female1', 'female_avatar.png')], default='default', max_length=8),
        ),
    ]
