from django.db import models
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    discounted_price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brands = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.name



# model for product variants 
class ColorVarient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.color}"


# model for product images
class ProductImage(models.Model):
    varient = models.ForeignKey(ColorVarient, on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return f'Images for {self.varient.product.name} {self.varient.color}'