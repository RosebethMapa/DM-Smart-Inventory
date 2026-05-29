from django.contrib import admin

from .models import Category, Product, Supplier


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "supplier", "current_stock", "reorder_level", "selling_price", "is_active")
    list_filter = ("is_active", "category", "supplier")
    search_fields = ("name", "sku", "barcode")


admin.site.register(Category)
admin.site.register(Supplier)
