from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Coupon(models.Model):
    """Модель купона"""
    code = models.CharField(max_length=100, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    active = models.BooleanField()

    def __str__(self):
        return self.code
