from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(
        upload_to='../media/product_images/')

    def __str__(self):
        return self.name
