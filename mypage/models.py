from django.db import models

from account.models import User
from product.models import Product
from order.models   import Order

class Mileage(models.Model):
    point = models.PositiveIntegerField(default=0)
    user  = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = "mileages"

class Question(models.Model):
    content   = models.CharField(max_length=1000)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user      = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = "questions"

class Answer(models.Model):
    content   = models.CharField(max_length=1000)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    seller    = models.CharField(max_length=20, default="seller")
    question  = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "answers"

class Favorite(models.Model):
    is_favorite = models.BooleanField(default=False)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "favorites"

class Review(models.Model):
    content     = models.CharField(max_length=2000)
    rating      = models.PositiveIntegerField()
    create_at   = models.DateTimeField(auto_now_add=True)
    update_at   = models.DateTimeField(auto_now=True)
    order       = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    recommander = models.ManyToManyField(
        User,
        through='reviewrecommand',
        through_fields=('review', 'user'),
        related_name='recommanded_user',
    )
    
    class Meta:
        db_table = "reviews"

class ReviewImage(models.Model):
    image_url = models.URLField(max_length=2000)
    review     = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "reviewimages"

class ReviewRecommand(models.Model):
    is_recommand = models.BooleanField(default=False)
    review       = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
    user         = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "reviewrecommands"