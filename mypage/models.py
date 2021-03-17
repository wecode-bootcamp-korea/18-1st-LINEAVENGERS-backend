from django.db import models

from account.models import User
from product.models import Product
from order.models   import Order

class Mileage(models.Model):
    point = models.IntegerField()
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "mileages"

class Question(models.Model):
    content   = models.CharField(max_length=1000)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "questions"

class Answer(models.Model):
    content   = models.CharField(max_length=1000)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    seller    = models.CharField(max_length=20, default="seller")
    question  = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        db_table = "answers"

class Favorite(models.Model):
    is_favorite = models.BooleanField(default=False)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "favorites"

class Review(models.Model):
    content   = models.CharField(max_length=2000)
    rating    = models.IntegerField()
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    order     = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    user      = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "reviews"

class Review_image(models.Model):
    image_url = models.URLField(max_length=2000)
    reviw     = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "review_images"

class Review_recommand(models.Model):
    is_recommand = models.BooleanField(default=False)
    reivew       = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
    user         = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "review_recommands"