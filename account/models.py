from django.db import models

class User(models.Model):
    login_id     = models.CharField(max_length=100)
    password     = models.CharField(max_length=100)
    name         = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=11)
    create_date  = models.DateField(auto_now_add=True)
    email        = models.CharField(max_length=50, null=True)
    user_image   = models.CharField(max_length=2000, null=True)
    is_active    = models.BooleanField(default=False)

    class Meta:
        db_table = "users"

