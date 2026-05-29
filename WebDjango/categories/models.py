from django.db import models
from products.models import Product

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField()
    products = models.ManyToManyField(Product)#relacion n * m
    create_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title