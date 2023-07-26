from django.contrib.auth.models import User
from django.db import models


class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    balance = models.DecimalField(default=0, max_digits=8, decimal_places=2)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField(null=False, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField()


class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # products = models.ManyToManyField(Product, related_name="orders")


class Item(models.Model):
    """
    Order's Item model.
    price individual for user or summarized with discount
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1, null=False)
    sum = models.DecimalField(default=0, max_digits=8, decimal_places=2)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    address = models.TextField(null=True, blank=True)
    bank_card = models.CharField(max_length=16)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

