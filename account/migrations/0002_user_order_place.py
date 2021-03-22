# Generated by Django 3.1.7 on 2021-03-22 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='order_place',
            field=models.ManyToManyField(related_name='place_users', through='order.Order', to='order.Address'),
        ),
    ]
