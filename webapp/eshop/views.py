from django.http import HttpRequest
from django.shortcuts import render
from .models import Product, Order


def shop_index(request: HttpRequest):
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999)
    ]
    context = {
        "products": products
    }
    return render(request, 'eshop/shop-index.html', context=context)


def product_list(request: HttpRequest):
    context = {
        "products": Product.objects.all(),
    }
    return render(request, 'eshop/product-list.html', context=context)


def order_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("items").all(),
    }
    return render(request, 'eshop/order-list.html', context=context)
