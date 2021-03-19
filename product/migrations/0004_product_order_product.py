# Generated by Django 3.1.7 on 2021-03-18 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        ('product', '0003_product_questioners'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='order_product',
            field=models.ManyToManyField(through='order.Cart', to='order.Order'),
        ),
    ]