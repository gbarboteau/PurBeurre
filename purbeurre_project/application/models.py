from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User


class Category(models.Model):
    """Model for the categories on the OpenFoodFacts
    API we want to add in our database
    """
    category_id = models.IntegerField(null=True)
    category_name = models.TextField()
    category_url = models.TextField()

class Aliment(models.Model):
    """Model for the aliments on the OpenFoodFacts API"""
    aliment_id = models.IntegerField(null=True)
    name = models.TextField()
    category = models.TextField()
    picture = models.TextField()
    nutriscore = models.TextField()
    description = models.TextField()
    stores = models.TextField()
    barcode = models.TextField()

class Substitute(models.Model):
    """Model for the substitutes, linked to a User
    and a given aliment
    """
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user_id', 'aliment_id'], name='saved_substitute')]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE,)
    aliment_id = models.ForeignKey(Aliment, on_delete=models.CASCADE,)
