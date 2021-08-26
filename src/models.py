from store.models import Order
from django.db import models
from store.models import *
# Create your models here.

class Razor(models.Model):
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    