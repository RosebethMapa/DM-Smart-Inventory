from django.contrib import admin

from .models import Payment, Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "cashier", "total_amount", "profit", "payment_method", "created_at", "is_void")
    list_filter = ("payment_method", "is_void", "created_at")
    inlines = [SaleItemInline]


admin.site.register(Payment)
