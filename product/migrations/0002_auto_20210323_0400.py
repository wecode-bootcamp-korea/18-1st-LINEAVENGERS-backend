# Generated by Django 3.1.7 on 2021-03-23 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(max_length=20),
        ),
    ]
