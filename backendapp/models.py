from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class product_categorytb(models.Model):
    id=models.AutoField(primary_key=True)
    category=models.CharField(max_length=100)

    def __str__(self):
        return self.category

class product_details(models.Model):
    id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=100)
    product_description=models.CharField(max_length=200)
    product_price=models.IntegerField()
    product_image=models.ImageField(upload_to='images/',null=True,
    blank=True)
    product_category=models.ForeignKey(product_categorytb, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
    

class Order(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=100)

    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    zipcode=models.CharField(max_length=100)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItems(models.Model):
   order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
   product=models.ForeignKey(product_details, on_delete=models.CASCADE)
   quantity = models.IntegerField() 
    

