from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.CharField(max_length=255)
    tools = models.CharField(max_length=255, default="Instapot")
    costs = models.CharField(max_length=255)
    procedure = models.TextField()
    notes = models.TextField()
    image_url = models.CharField(max_length = 200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Retailer(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    contact = models.CharField(max_length=255)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name

class Plant(models.Model):
    screen_name = models.CharField(max_length=255)
    image = models.CharField(max_length = 200, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    retailers= models.ManyToManyField(Retailer, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.screen_name




