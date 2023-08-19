from django.contrib.auth.models import User
from django.db import models


def avatar_path(instance: "Profile", filename: str) -> str:
    return "users/user_{pk}/avatar/{filename}".format(
        pk=instance.pk,
        filename=filename
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_path)


class Customer(Profile):
    address = models.TextField(null=True, blank=True)
    bank_card = models.CharField(max_length=16)


class Seller(Profile):
    balance = models.DecimalField(default=0, max_digits=8, decimal_places=2)
