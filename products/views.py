import json
from decimal import Decimal

from django.contrib import messages
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render

from sales.forms import SaleForm
from sales.services import create_sale
from dashboard.models import AuditLog
from accounts.decorators import role_required

from .forms import ProductForm
from .models import Category, Product, Supplier


@role_required("Owner", "Manager", "Staff")
def product_list(request):
    products = Product.objects.select_related("category", "supplier")
    order_form = SaleForm(request.POST or None)
    if request.method == "POST" and order_form.is_valid():
        try:
            raw_items = json.loads(order_form.cleaned_data["cart"])
            items = [{"product": get_object_or_404(Product, pk=row["id"]), "quantity": int(row["quantity"])} for row in raw_items]
            sale = create_sale(
                cashier=request.user,
                items=items,
                payment_method=order_form.cleaned_data["payment_method"],
                amount_received=order_form.cleaned_data["amount_received"],
                discount=order_form.cleaned_data["discount"] or Decimal("0.00"),
                customer_name=order_form.cleaned_data["customer_name"],
                customer_contact=order_form.cleaned_data["customer_contact"],
                status=order_form.cleaned_data["order_status"],
            )
            messages.success(request, "Order saved.")
            return redirect("receipt", pk=sale.pk)
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            order_form.add_error(None, str(exc))

    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    selected_category = request.GET.get("category", "")
    selected_supplier = request.GET.get("supplier", "")
    if query:
        products = products.filter(Q(name__icontains=query) | Q(sku__icontains=query) | Q(barcode__icontains=query))
    if selected_category:
        products = products.filter(category_id=selected_category)
    if selected_supplier:
        products = products.filter(supplier_id=selected_supplier)
    if status == "low":
        products = products.filter(current_stock__lte=F("reorder_level"), current_stock__gt=0)
    elif status == "out":
        products = products.filter(current_stock__lte=0)
    elif status == "archived":
        products = products.filter(is_active=False)
    else:
        products = products.filter(is_active=True)
    featured_product = products.exclude(image="").first() or products.exclude(image_url="").first() or products.first()
    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "featured_product": featured_product,
            "order_form": order_form,
            "query": query,
            "status": status,
            "categories": Category.objects.all(),
            "suppliers": Supplier.objects.filter(is_active=True),
            "selected_category": selected_category,
            "selected_supplier": selected_supplier,
        },
    )


@role_required("Owner", "Manager")
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        product = form.save()
        AuditLog.objects.create(user=request.user, action="product_created", table_affected="products", record_id=str(product.pk))
        messages.success(request, "Product added.")
        return redirect("product_list")
    return render(request, "products/product_form.html", {"form": form, "title": "Add product"})


@role_required("Owner", "Manager")
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        product = form.save()
        AuditLog.objects.create(user=request.user, action="product_edited", table_affected="products", record_id=str(product.pk))
        messages.success(request, "Product updated.")
        return redirect("product_list")
    return render(request, "products/product_form.html", {"form": form, "title": "Edit product", "product": product})


@role_required("Owner")
def product_archive(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.is_active = False
        product.save(update_fields=["is_active", "updated_at"])
        AuditLog.objects.create(user=request.user, action="product_archived", table_affected="products", record_id=str(product.pk))
        messages.success(request, "Product archived.")
    return redirect("product_list")
