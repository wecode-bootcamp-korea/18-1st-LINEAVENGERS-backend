from django.db import models

from product.models import Product, Product_size
from account.models import User

class Order_address(models.Model):
    receiver       = models.CharField(max_length=50)
    nickname       = models.CharField(max_length=200, null=True)
    address        = models.CharField(max_length=200)
    first_contact  = models.CharField(max_length=11)
    second_contact = models.CharField(max_length=11, null=True)
    memo           = models.CharField(max_length=500, null=True)
    is_default     = models.BooleanField(default=True)
    user           = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "order_addresses"

class Order_status(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "order_statuses"

class Pay_type(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "pay_types"

class Order(models.Model):
    order_no     = models.CharField(max_length=30, unique=True)
    order_at     = models.DateField(auto_now_add=True)
    order_status = models.ForeignKey(Order_status, on_delete=models.CASCADE, null=True)
    user         = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address      = models.ForeignKey(Order_address, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "orders"

class Order_product(models.Model):
    quantity      = models.IntegerField()
    product       = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order         = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product_size  = models.ForeignKey(Product_size, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "order_products"

class Payment(models.Model):
    pay_at   = models.DateField(auto_now_add=True)
    result   = models.CharField(max_length=200)
    pay_type = models.ForeignKey(Pay_type, on_delete=models.CASCADE, null=True)
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "payments"

class Cart(models.Model):
    quantity     = models.IntegerField()
    user         = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product_size = models.ForeignKey(Product_size, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "carts"