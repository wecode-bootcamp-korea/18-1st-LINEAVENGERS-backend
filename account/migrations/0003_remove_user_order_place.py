# Generated by Django 3.1.7 on 2021-03-19 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_order_place'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='order_place',
        ),
    ]
