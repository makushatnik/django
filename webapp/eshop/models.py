from django.contrib.auth.models import User
from django.db import models


def product_preview_path(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename
    )


def product_image_path(instance: "ProductImage", filename: str) -> str:
    return "products/product_{pk}/image/{filename}".format(
        pk=instance.product.pk,
        filename=filename
    )


class Seller(models.Model):
    """
    User who signed up as a Seller.
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    balance = models.DecimalField(default=0, max_digits=8, decimal_places=2)


class Category(models.Model):
    """
    Product's Category model.
    """
    name = models.CharField(max_length=100)


class Product(models.Model):
    """
    Product for buying/selling in Webapp.
    """
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField(null=False, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_path)
    archived = models.BooleanField()

    @property
    def description_short(self) -> str:
        if len(self.description) < 48:
            return self.description
        return self.description[:48] + "..."

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    description = models.CharField(max_length=200, null=False, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=product_image_path)


class Order(models.Model):
    """
    Order model.
    Contains product Item's.
    """
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    receipt = models.FileField(null=True, upload_to='order/receipts')
    # products = models.ManyToManyField(Product, related_name="orders")


class Item(models.Model):
    """
    Order's Item model.
    price is individual for user or summarized with discount
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1, null=False)
    sum = models.DecimalField(default=0, max_digits=8, decimal_places=2)


class Customer(models.Model):
    """
    User who signed up as a Customer.
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    address = models.TextField(null=True, blank=True)
    bank_card = models.CharField(max_length=16)


class Review(models.Model):
    """
    Customer' Review on a Product.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

