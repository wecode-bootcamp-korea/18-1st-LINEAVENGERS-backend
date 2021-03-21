from django.db import models

from account.models import User

class Menu(models.Model):
    name = models.CharField(max_length=30)
    no   = models.CharField(max_length=5, unique=True)
    class Meta:
        db_table = "menus"

class Category(models.Model):
    name = models.CharField(max_length=50)
    no   = models.CharField(max_length=5)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        db_table = "categories"

class Size(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "sizes"

class Product(models.Model):
    name             = models.CharField(max_length=100)
    price            = models.DecimalField(max_digits=10, decimal_places=2)
    create_at        = models.DateTimeField(auto_now_add=True)
    update_at        = models.DateTimeField(auto_now=True)
    content          = models.TextField(null=True)
    is_best          = models.BooleanField(default=False)
    is_new           = models.BooleanField(default=True)
    is_free_shipping = models.BooleanField(default=False)
    is_soldout       = models.BooleanField(default=False)
    discount_rate    = models.DecimalField(max_digits=5, decimal_places=2)
    category         = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    sizes            = models.ManyToManyField(
        Size,
        through='ProductSize',
        through_fields=('product', 'size'),
        related_name='size_products',
    )
    questioners      = models.ManyToManyField(
        User,
        through='mypage.Question',
        through_fields=('product', 'user'),
        related_name='questioned_products',
    )
    product_orders   = models.ManyToManyField(
        'order.Order',
        through='order.Cart',
        through_fields=('product', 'order'),
        related_name='ordered_products',
    )
    follwers          = models.ManyToManyField(
        User,
        through='mypage.Favorite',
        through_fields=('product', 'user'),
        related_name='followed_products',
    )
    reviewers          = models.ManyToManyField(
        User,
        through='mypage.Review',
        through_fields=('product', 'user'),
        related_name='reviewed_products',
    )
    
    class Meta:
        db_table = "products"

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    size    = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "productsizes"

class ProductImage(models.Model):
    image_url    = models.URLField(max_length=2000)
    is_thumbnail = models.BooleanField(default=False)
    product      = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "productimages"
