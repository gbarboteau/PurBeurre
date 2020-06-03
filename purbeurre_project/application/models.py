from django.db import models
from django.forms import ModelForm

# Create your models here.

class Product(models.Model):
    product_id = models.IntegerField(null=True)
    name = models.TextField()
    category = models.TextField()
    picture = models.TextField()
    nutriscore = models.TextField()
    description = models.TextField()
    stores = models.TextField()


class User(models.Model):
    reference = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.TextField()
    email = models.TextField()
    password = models.TextField()
