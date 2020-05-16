from django.db import models

# Create your models here.
class User(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    type = models.CharField(max_length=3)


class Toppings(models.Model):
    Topping = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.Topping}"


class Regular_Pizza(models.Model):
    Regular_Pizza = models.CharField(max_length=64)
    Topz = models.ManyToManyField(Toppings, blank=True, related_name="Rtopz")

    def __str__(self):
        return f"{self.Regular_Pizza}"


class Sicilian_Pizza(models.Model):
    Sicilian_Pizza = models.CharField(max_length=64)
    Tops = models.ManyToManyField(Toppings, blank=True, related_name="Stopz")

    def __str__(self):
        return f"{self.Sicilian_Pizza}"


class Subs(models.Model):
    Sub = models.CharField
    Price = models.FloatField()

    def __str__(self):
        return f"{self.Sub}"


class Salads(models.Model):
    Salad = models.CharField(max_length=64)
    Price = models.FloatField()

    def __str__(self):
        return f"{self.Salad}"


class Pasta(models.Model):
    Pasta = models.CharField(max_length=64)
    Price = models.FloatField()

    def __str__(self):
        return f"{self.Pasta}"


class Dinner_Platters(models.Model):
    Platter = models.CharField(max_length=64)
    Tops = models.ManyToManyField(Toppings, related_name="Dtopz")

    def __str__(self):
        return f"{self.Platter}"
