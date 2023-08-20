from typing import Sequence
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction
from eshop.models import Product, Order


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Order creation")
        user = User.objects.get(username='admin')
        products: Sequence[Product] = Product.objects.only('id').all()
        order, created = Order.objects.get_or_create(
            delivery_address='Test Address',
            promocode='SALE123',
            user=user
        )
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(f"Created order {order}")
