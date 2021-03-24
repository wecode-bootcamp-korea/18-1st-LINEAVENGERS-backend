# Generated by Django 3.1.7 on 2021-03-24 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(max_length=200)),
                ('first_contact', models.CharField(max_length=11)),
                ('second_contact', models.CharField(max_length=11, null=True)),
                ('memo', models.CharField(max_length=500, null=True)),
                ('is_default', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'orderstatuses',
            },
        ),
        migrations.CreateModel(
            name='PayType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'paytypes',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('result', models.CharField(max_length=200)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('pay_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.paytype')),
            ],
            options={
                'db_table': 'payments',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='order_paytypes',
            field=models.ManyToManyField(related_name='paytype_orders', through='order.Payment', to='order.PayType'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.orderstatus'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.user'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
            options={
                'db_table': 'carts',
            },
        ),
    ]
