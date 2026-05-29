import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from dashboard.models import BusinessSettings
from products.models import Category, Product

from .forms import CustomerOrderForm, SaleForm
from .models import Sale
from .services import create_sale, update_order_status


def _system_cashier():
    User = get_user_model()
    return (
        User.objects.filter(username="admin").first()
        or User.objects.filter(is_superuser=True).first()
        or User.objects.first()
    )


def customer_order(request):
    products = Product.objects.filter(is_active=True, current_stock__gt=0).select_related("category").order_by("name")
    categories = Category.objects.filter(products__is_active=True, products__current_stock__gt=0).distinct().order_by("name")
    form = CustomerOrderForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            raw_items = json.loads(form.cleaned_data["cart"])
            cashier = _system_cashier()
            if not cashier:
                raise ValueError("No admin account is available to receive orders.")
            items = [{"product": get_object_or_404(Product, pk=row["id"]), "quantity": int(row["quantity"])} for row in raw_items]
            sale = create_sale(
                cashier=cashier,
                items=items,
                payment_method="cash",
                amount_received=Decimal("0.00"),
                discount=Decimal("0.00"),
                customer_name=form.cleaned_data["customer_name"],
                customer_contact=form.cleaned_data["customer_contact"],
                status=Sale.STATUS_PENDING,
            )
            return redirect("customer_order_success", pk=sale.pk)
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            form.add_error(None, str(exc))

    return render(request, "sales/customer_order.html", {"products": products, "categories": categories, "form": form})


def customer_order_success(request, pk):
    sale = get_object_or_404(Sale.objects.prefetch_related("items__product"), pk=pk)
    return render(request, "sales/customer_order_success.html", {"sale": sale})


@role_required("Owner", "Manager", "Staff")
def pos(request):
    products = Product.objects.filter(is_active=True).select_related("category", "supplier").order_by("name")
    form = SaleForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            raw_items = json.loads(form.cleaned_data["cart"])
            items = [{"product": get_object_or_404(Product, pk=row["id"]), "quantity": int(row["quantity"])} for row in raw_items]
            sale = create_sale(
                cashier=request.user,
                items=items,
                payment_method=form.cleaned_data["payment_method"],
                amount_received=form.cleaned_data["amount_received"],
                discount=form.cleaned_data["discount"] or Decimal("0.00"),
                customer_name=form.cleaned_data["customer_name"],
                customer_contact=form.cleaned_data["customer_contact"],
                status=form.cleaned_data["order_status"],
            )
            messages.success(request, "Order saved.")
            return redirect("receipt", pk=sale.pk)
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            form.add_error(None, str(exc))
    return render(request, "sales/pos.html", {"products": products, "form": form})


@role_required("Owner", "Manager", "Staff")
def order_menu(request):
    return redirect("product_list")


@role_required("Owner", "Manager", "Staff")
def order_history(request):
    status = request.GET.get("status", "")
    orders = Sale.objects.select_related("cashier").prefetch_related("items__product").order_by("-created_at")
    if status:
        orders = orders.filter(status=status)
    return render(request, "sales/order_history.html", {"orders": orders[:60], "status": status, "status_choices": Sale.STATUS_CHOICES})


@role_required("Owner", "Manager", "Staff")
def set_order_status(request, pk, status):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == "POST":
        try:
            update_order_status(sale=sale, status=status, user=request.user)
            messages.success(request, "Order status updated.")
        except ValueError as exc:
            messages.error(request, str(exc))
    return redirect("order_history")


@role_required("Owner", "Manager", "Staff")
def receipt(request, pk):
    sale = get_object_or_404(Sale.objects.select_related("cashier").prefetch_related("items__product"), pk=pk)
    business = BusinessSettings.objects.first()
    return render(request, "sales/receipt.html", {"sale": sale, "business": business})


@role_required("Owner", "Manager", "Staff")
def product_lookup(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.filter(is_active=True)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(sku__icontains=query) | Q(barcode__icontains=query))
    data = [
        {
            "id": p.pk,
            "name": p.name,
            "sku": p.sku,
            "price": str(p.selling_price),
            "stock": p.current_stock,
            "unit": p.unit_type,
            "image": p.image_src,
        }
        for p in products[:20]
    ]
    return JsonResponse({"products": data})
