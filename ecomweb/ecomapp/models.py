from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    productname = models.CharField(max_length=100)
    prize = models.IntegerField()
    offer = models.CharField(max_length=50)
    speed = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='images/')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products_sold')

class Verify(models.Model):
    otp = models.IntegerField()
    otp1 = models.IntegerField()

class Categories(models.Model):
    category = models.CharField(max_length=50)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
 cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
 product = models.ForeignKey(Product, on_delete=models.CASCADE)
    

