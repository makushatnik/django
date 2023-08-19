from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Product, ProductImage, Order, Item


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
class ProductAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
        mark_unarchived
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
