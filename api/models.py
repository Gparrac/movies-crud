from django.core.validators import MaxValueValidator, MinValueValidator

from django.db import models

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    score = models.DecimalField(max_digits=2, decimal_places=1,validators=[MaxValueValidator(5), MinValueValidator(0)])
