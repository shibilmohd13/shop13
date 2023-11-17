from django.db import models
# Create your models here.


# Model for categories
class Category(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Model for Brands
class Brand(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# model for products
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
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
    price = models.IntegerField()
    is_listed = models.BooleanField(default=True)
    product_offer = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    category_offer = models.DecimalField(max_digits=5, decimal_places=2, default=0)


    def discount(self):
        discount_percentage = 0

        if self.product_offer > self.category_offer:
            
            discount_percentage = self.product_offer
        else:
            discount_percentage = self.category_offer
            
        return discount_percentage

    
    def discounted_price(self):
        if self.discount() > 0:
            return self.price - ((self.price * self.discount()) / 100)
        else:
            return self.price

    def __str__(self):
        return f"{self.product.name} - {self.color}"


# model for product images
class ProductImage(models.Model):
    varient = models.ForeignKey(ColorVarient, on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return f'Images for {self.varient.product.name} {self.varient.color}'
