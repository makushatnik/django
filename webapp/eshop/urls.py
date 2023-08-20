from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter
from webapp.settings import CACHE_MIDDLEWARE_SECONDS
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
    ProductViewSet,
    LatestProductsFeed
)

app_name = "eshop"

router = DefaultRouter()
router.register("products", ProductViewSet)

urlpatterns = [
    path('', cache_page(CACHE_MIDDLEWARE_SECONDS)(ShopIndexView.as_view()), name='index'),
    path('api/', include(router.urls)),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/export/', ProductDataExportView.as_view(), name='product_export'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_detail'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archive', ProductDeleteView.as_view(), name='product_delete'),
    path('products/latest/feed/', LatestProductsFeed(), name='products-feed'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
]
