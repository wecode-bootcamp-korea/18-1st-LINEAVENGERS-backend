# Generated by Django 3.1.7 on 2021-03-19 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypage', '0003_auto_20210319_1048'),
        ('account', '0003_remove_user_order_place'),
        ('product', '0006_auto_20210318_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='no',
            field=models.CharField(default='', max_length=5),
        ),
        migrations.AddField(
            model_name='menu',
            name='no',
            field=models.CharField(default='', max_length=5, unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='reviewers',
            field=models.ManyToManyField(related_name='reviewed_products', through='mypage.Review', to='account.User'),
        ),
        migrations.AlterField(
            model_name='product',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='follwers',
            field=models.ManyToManyField(related_name='followed_products', through='mypage.Favorite', to='account.User'),
        ),
    ]
