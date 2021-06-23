from django.contrib import admin

from .models import Topping, Regular_Pizza, Sicilian_Pizza, Subs, Salads, Pasta, Dinner_Platters

# Register your models here.
# admin.site.register(User)
admin.site.register(Topping)
admin.site.register(Regular_Pizza)
admin.site.register(Sicilian_Pizza)
admin.site.register(Subs)
admin.site.register(Salads)
admin.site.register(Pasta)
admin.site.register(Dinner_Platters)
