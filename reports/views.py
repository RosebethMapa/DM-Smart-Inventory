from datetime import timedelta

from django.db.models import Count, DecimalField, F, Sum
from django.db.models.functions import Coalesce, TruncDate, TruncMonth, TruncWeek
from django.shortcuts import render
from django.utils import timezone

from accounts.decorators import role_required
from products.models import Product
from sales.models import Sale, SaleItem
from stock.models import StockMovement


@role_required("Owner", "Manager")
def reports_home(request):
    money = DecimalField(max_digits=14, decimal_places=2)
    today = timezone.localdate()
    default_start = today - timedelta(days=13)
    start_date = request.GET.get("start") or default_start.isoformat()
    end_date = request.GET.get("end") or today.isoformat()

    sales = Sale.objects.filter(is_void=False)
    filtered_sales = sales.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)
    daily = (
        filtered_sales.annotate(period=TruncDate("created_at"))
        .values("period")
        .annotate(
            orders=Count("id"),
            total=Coalesce(Sum("total_amount"), 0, output_field=money),
            cost=Coalesce(Sum("total_cost"), 0, output_field=money),
            profit=Coalesce(Sum("profit"), 0, output_field=money),
        )
        .order_by("-period")
    )
    weekly = filtered_sales.annotate(period=TruncWeek("created_at")).values("period").annotate(total=Sum("total_amount"), profit=Sum("profit")).order_by("-period")[:8]
    monthly = filtered_sales.annotate(period=TruncMonth("created_at")).values("period").annotate(total=Sum("total_amount"), profit=Sum("profit")).order_by("-period")[:12]
    best_sellers = SaleItem.objects.filter(sale__in=filtered_sales).values("product__name").annotate(units=Sum("quantity"), revenue=Sum("line_total")).order_by("-units")[:10]
    low_stock = Product.objects.filter(is_active=True, current_stock__lte=F("reorder_level")).select_related("supplier")[:20]
    movements = StockMovement.objects.select_related("product", "supplier", "created_by")[:30]
    summary = filtered_sales.aggregate(
        orders=Count("id"),
        revenue=Coalesce(Sum("total_amount"), 0, output_field=money),
        cost=Coalesce(Sum("total_cost"), 0, output_field=money),
        profit=Coalesce(Sum("profit"), 0, output_field=money),
    )
    pending_orders = Sale.objects.filter(status=Sale.STATUS_PENDING, is_void=False)[:12]
    recent_sales = filtered_sales.select_related("cashier").prefetch_related("items__product").order_by("-created_at")[:40]
    return render(request, "reports/reports.html", {
        "daily": daily,
        "weekly": weekly,
        "monthly": monthly,
        "best_sellers": best_sellers,
        "low_stock": low_stock,
        "movements": movements,
        "summary": summary,
        "pending_orders": pending_orders,
        "recent_sales": recent_sales,
        "start_date": start_date,
        "end_date": end_date,
    })
