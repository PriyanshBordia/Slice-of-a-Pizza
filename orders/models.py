from django.core import validators
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.Topping}"


class Regular_Pizza(models.Model):
    
    Regular_Pizza = models.CharField(max_length=64)
    Price = models.FloatField(validators=[MinValueValidator(1)], blank=False, null=False)
    
    toppings = models.ManyToManyField(Topping, blank=True, related_name="addons")

    def __str__(self):
        return f"{self.Regular_Pizza}"


class Sicilian_Pizza(models.Model):

    Sicilian_Pizza = models.CharField(max_length=64)
    Price = models.FloatField(validators=[MinValueValidator(1)], blank=False, null=False)

    Tops = models.ManyToManyField(Topping, blank=True, related_name="addons")

    def __str__(self):
        return f"{self.Sicilian_Pizza}"


class Subs(models.Model):
    Sub = models.CharField
    Price = models.FloatField()

    def __str__(self):
        return f"{self.Sub}"


class Salads(models.Model):

    Salad = models.CharField(max_length=64)
    Price = models.FloatField(validators=[MinValueValidator(1)], blank=False, null=False)


    def __str__(self):
        return f"{self.Salad}"


class Pasta(models.Model):
   
    Pasta = models.CharField(max_length=64)
    Price = models.FloatField(validators = [MinValueValidator(1)] ,blank=False, null=False)

    def __str__(self):
        return f"{self.Pasta}"


class Dinner_Platters(models.Model):

    Platter = models.CharField(max_length=64)
    Tops = models.ManyToManyField(Toppings, related_name="addons")

    def __str__(self):
        return f"{self.Platter}"
