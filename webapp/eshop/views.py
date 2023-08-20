import logging
from csv import DictWriter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from webapp.settings import CACHE_MIDDLEWARE_SECONDS

from .forms import ProductForm
from .models import Product, ProductImage, Order
from .serializers import ProductSerializer
from .utils import save_csv_products

log = logging.getLogger(__name__)

PRODUCT_EXPORT_CACHE_KEY = "products_data_export"


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(archived=False)
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived"
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):
        filename = "products-export.csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f"attachment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })

        return response

    @action(
        methods=["post"],
        detail=False,
        parser_classes=[MultiPartParser]
    )
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            request.encoding
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999)
        ]
        context = {
            "products": products
        }
        return render(request, 'eshop/shop-index.html', context=context)


class ProductListView(ListView):
    template_name = 'eshop/product/list.html'
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


@cache_page(CACHE_MIDDLEWARE_SECONDS)
class ProductDetailsView(DetailView):
    template_name = 'eshop/product/detail.html'
    context_object_name = "product"
    queryset = Product.objects.filter(archived=False).prefetch_related("images")


class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = 'eshop/product/form.html'
    model = Product
    success_url = reverse_lazy('eshop:product:list')
    form_class = ProductForm

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image
            )
        return response


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'eshop/product/update_form.html'
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('eshop:product_details', kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image
            )
        return response


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('eshop:product_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return redirect(success_url)


# def create_product(request: HttpRequest):
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             Product.objects.create(**form.cleaned_data)
#             url = reverse("eshop:product_list")
#             return redirect(url)
#     else:
#         form = ProductForm()
#
#     context = {
#         "form": form
#     }
#     return render(request, 'eshop/product/create.html', context=context)


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'eshop/order/list.html'
    context_object_name = "orders"
    queryset = (
        Order.objects.select_related("user").prefetch_related("items")
    )


@cache_page(CACHE_MIDDLEWARE_SECONDS)
class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "eshop.view_order"
    template_name = 'eshop/order/list.html'
    context_object_name = "order"
    queryset = (
        Order.objects.select_related("user").prefetch_related("items")
    )


class ProductDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products_data = cache.get(PRODUCT_EXPORT_CACHE_KEY)
        if not products_data:
            products = Product.objects.order_by("pk").all()
            products_data = [
                {
                    "pk": product.pk,
                    "name": product.name,
                    "price": str(product.price),
                    "archived": product.archived
                }
                for product in products
            ]
            cache.set(PRODUCT_EXPORT_CACHE_KEY, products_data, CACHE_MIDDLEWARE_SECONDS)
        return JsonResponse({"products": products_data})


class LatestProductsFeed(Feed):
    title = "Products (latest)"
    description = "Updates on changes & addition of products"
    link = reverse_lazy('eshop:products')

    def items(self):
        return (
            Product.objects
            .filter(archived=False)
            .order_by("-created_at")[:5]
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]
