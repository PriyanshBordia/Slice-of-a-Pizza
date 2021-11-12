from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Topping(models.Model):
	name = models.CharField(max_length=64)
	
	slug = models.SlugField(max_length=64, unique=True, default=1)

	def __str__(self):
		return f"{self.Topping}"

class Order(models.Model):

	Pizza = 1
	


class Regular_Pizza(models.Model):
	
	Regular_Pizza = models.CharField(max_length=64)
	Price = models.FloatField(validators=[MinValueValidator(1)], blank=False, null=False, default=1)
	
	toppings = models.ManyToManyField(Topping, blank=True, related_name="rpAddons")
	slug = models.SlugField(max_length=64, unique=True, default=1)

	def __str__(self):
		return f"{self.Regular_Pizza}"


class Sicilian_Pizza(models.Model):

	Sicilian_Pizza = models.CharField(max_length=64)
	Price = models.FloatField(validators=[MinValueValidator(1)], blank=False, null=False, default=1)

	Tops = models.ManyToManyField(Topping, blank=True, related_name="spAddons")

	slug = models.SlugField(max_length=64, unique=True, default=1)

	def __str__(self):
		return f"{self.Sicilian_Pizza}"


class Subs(models.Model):
	Sub = models.CharField
	Price = models.FloatField()

	slug = models.SlugField(max_length=64, unique=True, default=1)

	def __str__(self):
		return f"{self.Sub}"


class Salads(models.Model):

	Salad = models.CharField(max_length=64)
	Price = models.FloatField(validators=[MinValueValidator(1)], blank=False, null=False, default=1)

	slug = models.SlugField(max_length=64, unique=True, default=1)

	def __str__(self):
		return f"{self.Salad}"


class Pasta(models.Model):
   
	Pasta = models.CharField(max_length=64)
	Price = models.FloatField(validators = [MinValueValidator(1)] ,blank=False, null=False)

	slug = models.SlugField(max_length=64, unique=True, default=9)

	def __str__(self):
		return f"{self.Pasta}"


class Dinner_Platters(models.Model):

	Platter = models.CharField(max_length=64)
	Tops = models.ManyToManyField(Topping, related_name="DPAddons")

	slug = models.SlugField(max_length=64, unique=True, default=10)

	def __str__(self):
		return f"{self.Platter}"
