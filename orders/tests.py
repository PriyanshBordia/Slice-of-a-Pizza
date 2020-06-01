from django.db.models import MAX
from django.test import TestCase

from .models import User, Toppings, Regular_Pizza, Sicilian_Pizza, Subs, Salads, Pasta, Dinner_Platters

# Create your tests here.

class ModelsTestCase(TestCase):

    def setUp(self):
