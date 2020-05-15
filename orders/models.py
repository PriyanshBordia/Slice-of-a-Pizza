from django.db import models

# Create your models here.
class Regular_Pizza(models.Model):


class Subs(models.Model):
    Sub = models.CharField

class Salads(models.Model):
    Salad = models.CharField(max_length=64)

class Pasta(models.Model):
    Pasta = models.CharField(max_length=64)
    Price = models.RealField()

class DinnerPlatters(models.Model):
    Platter
    Small = models.BooleanField(blank=True)
    Large = models.BooleanField(blank=True)
    Tops = models.ManyToManyField(Toppings, relates_name)

class Toppings(models.Model):
    Topping = models.CharField(max_length=64)
