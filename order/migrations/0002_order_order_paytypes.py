# Generated by Django 3.1.7 on 2021-03-18 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_paytypes',
            field=models.ManyToManyField(related_name='paytype_orders', through='order.Payment', to='order.PayType'),
        ),
    ]
