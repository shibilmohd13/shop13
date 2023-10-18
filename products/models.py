from django.db import models
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField()

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField()

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brands = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='products')
    image2 = models.ImageField(upload_to='products')
    image3 = models.ImageField(upload_to='products')
    is_listed = models.BooleanField()

    def __str__(self):
        return self.name

