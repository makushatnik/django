from django.contrib import admin
from django.contrib.auth.models import User
from .models import Product, Order


def get_full_name(user: User):
    full_name = f"{user.first_name} {user.last_name}"
    full_name = full_name.split()
    return full_name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
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
        ("Extra options", {
            "fields": ("archived",),
            "classes": ("collapse",),
        })
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("items")

    def user_verbose(self, obj: Order) -> str:
        return get_full_name(obj.user) or obj.user.username
