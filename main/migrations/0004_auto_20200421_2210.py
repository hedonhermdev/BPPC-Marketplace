# Generated by Django 2.2.10 on 2020-04-21 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200420_2345'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ProductReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('reason', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField()),
            ],
        ),
        migrations.RenameModel(
            old_name='QuesAndAnswer',
            new_name='ProductQnA',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='no_of_ratings',
            new_name='num_ratings',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Category'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.Product'),
        ),
        migrations.DeleteModel(
            name='RateUsers',
        ),
        migrations.AddField(
            model_name='userrating',
            name='rating_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings_given', to='main.Profile'),
        ),
        migrations.AddField(
            model_name='userrating',
            name='rating_for',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings_recieved', to='main.Profile'),
        ),
        migrations.AddField(
            model_name='productreport',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='main.Product'),
        ),
        migrations.AddField(
            model_name='productreport',
            name='reported_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='main.Profile'),
        ),
    ]