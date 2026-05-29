from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from products.models import Product
from sales.models import Sale, SaleItem
from stock.models import StockMovement


def calculate_dashboard_metrics():
    today = timezone.localdate()
    products = Product.objects.filter(is_active=True)
    today_sales = Sale.objects.filter(created_at__date=today, is_void=False)
    money = DecimalField(max_digits=14, decimal_places=2)

    stock_value_expr = ExpressionWrapper(F("current_stock") * F("cost_price"), output_field=money)
    stock_value = products.aggregate(total=Coalesce(Sum(stock_value_expr), 0, output_field=money))["total"]

    return {
        "total_products": products.count(),
        "stock_value": stock_value,
        "today_sales": today_sales.aggregate(total=Coalesce(Sum("total_amount"), 0, output_field=money))["total"],
        "profit_today": today_sales.aggregate(total=Coalesce(Sum("profit"), 0, output_field=money))["total"],
        "low_stock_count": products.filter(current_stock__gt=0, current_stock__lte=F("reorder_level")).count(),
        "out_of_stock_count": products.filter(current_stock__lte=0).count(),
        "pending_orders": Sale.objects.filter(status=Sale.STATUS_PENDING, is_void=False).count(),
        "low_stock_products": products.filter(current_stock__lte=F("reorder_level")).select_related("supplier", "category")[:8],
        "recent_movements": StockMovement.objects.select_related("product", "created_by")[:8],
        "recent_sales": Sale.objects.select_related("cashier").prefetch_related("items")[:6],
        "fast_moving_products": (
            SaleItem.objects.filter(sale__created_at__date=today, sale__is_void=False)
            .values("product__name")
            .annotate(units=Sum("quantity"), lines=Count("id"))
            .order_by("-units")[:5]
        ),
    }


def generate_low_stock_report():
    return Product.objects.filter(is_active=True, current_stock__lte=F("reorder_level")).select_related("supplier", "category")
