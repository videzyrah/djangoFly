from django.contrib import admin

# Register your models here.
from .models import Recipe, Retailer, Plant

admin.site.register(Recipe)
admin.site.register(Retailer)
admin.site.register(Plant)

