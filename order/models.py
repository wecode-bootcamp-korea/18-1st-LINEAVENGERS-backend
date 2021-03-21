from django.db import models

from product.models import Product, Size
from account.models import User

class Address(models.Model):
    receiver       = models.CharField(max_length=50)
    nickname       = models.CharField(max_length=200, null=True)
    address        = models.CharField(max_length=200)
    first_contact  = models.CharField(max_length=11)
    second_contact = models.CharField(max_length=11, null=True)
    memo           = models.CharField(max_length=500, null=True)
    is_default     = models.BooleanField(default=True)
    user           = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "addresses"

class OrderStatus(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "orderstatuses"

class PayType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "paytypes"

class Payment(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    result    = models.CharField(max_length=200)
    pay_type  = models.ForeignKey(PayType, on_delete=models.CASCADE, null=True)
    order     = models.ForeignKey('Order', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "payments"

class Order(models.Model):
    order_no       = models.CharField(max_length=30, unique=True)
    create_at      = models.DateTimeField(auto_now_add=True)
    order_status   = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, null=True)
    user           = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_paytypes = models.ManyToManyField(
        PayType,
        through='payment',
        through_fields=('order', 'pay_type'),
        related_name='paytype_orders',
    )

    class Meta:
        db_table = "orders"

class Cart(models.Model):
    quantity = models.PositiveIntegerField()
    product  = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    size     = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "carts"