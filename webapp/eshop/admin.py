from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm
from .models import Product, ProductImage, Order, Item
from .utils import save_csv_products


def get_full_name(user: User):
    full_name = f"{user.first_name} {user.last_name}"
    full_name = full_name.split()
    return full_name


# class OrderInline(admin.TabularInline):
#     model = Item.order.through


class ProductInline(admin.StackedInline):
    model = ProductImage


@admin.action(description="Archive products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = 'eshop/products/changelist.html'
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv"
    ]
    inlines = [
        ProductInline
    ]
    list_display = "pk", "name", "category", "description_short", "price", "discount"
    list_display_links = "pk", "name"
    ordering = "pk",
    search_fields = "name", "description"
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("collapse",),
        }),
        ("Images", {
            "fields": ("preview",),
        }),
        ("Extra options", {
            "fields": ("archived",),
            "classes": ("collapse",),
        })
    ]

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            return render(request, 'admin/csv_form.html', {"form": form})
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'admin/csv_form.html', {"form": form}, status=400)

        save_csv_products(form.files["csv_file"].file, request.encoding)
        self.message_user(request, 'Data from CSV were imported')
        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('import-products-csv/', self.import_csv, name='import_products_csv')
        ]
        return new_urls + urls


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "order", "price", "quantity", "sum"
    # inlines = [
    #     OrderInline
    # ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("items")

    def user_verbose(self, obj: Order) -> str:
        return get_full_name(obj.user) or obj.user.username
