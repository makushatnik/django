from django.urls import path
from .views import shop_index, product_list, order_list

app_name = "eshop"

urlpatterns = [
    path('', shop_index, name='index'),
    path('products/', product_list, name='products'),
    path('orders/', order_list, name='orders')
]
