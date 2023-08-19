from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShopIndexView,
    ProductListView,
    ProductDetailsView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderListView,
    OrderDetailView,
    ProductDataExportView,
    ProductViewSet
)

app_name = "eshop"

router = DefaultRouter()
router.register("products", ProductViewSet)

urlpatterns = [
    path('', ShopIndexView.as_view(), name='index'),
    path('api/', include(router.urls)),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/export/', ProductDataExportView.as_view(), name='product_export'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_detail'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archive', ProductDeleteView.as_view(), name='product_delete'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order_detail')
]
