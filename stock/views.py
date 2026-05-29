from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.decorators import role_required
from dashboard.services import generate_low_stock_report

from .forms import StockAdjustmentForm, StockInForm
from .models import StockMovement
from .services import add_stock, adjust_stock


@role_required("Owner", "Manager", "Staff")
def stock_in(request):
    form = StockInForm(request.POST or None)
    if form.is_valid():
        try:
            add_stock(user=request.user, **form.cleaned_data)
            messages.success(request, "Stock added and movement recorded.")
            return redirect("stock_movements")
        except ValueError as exc:
            form.add_error(None, str(exc))
    return render(request, "stock/stock_in.html", {"form": form})


@role_required("Owner", "Manager")
def stock_adjustment(request):
    form = StockAdjustmentForm(request.POST or None)
    if form.is_valid():
        try:
            adjust_stock(user=request.user, **form.cleaned_data)
            messages.success(request, "Stock adjustment saved.")
            return redirect("stock_movements")
        except ValueError as exc:
            form.add_error(None, str(exc))
    return render(request, "stock/adjustment.html", {"form": form})


@login_required
def stock_movements(request):
    movements = StockMovement.objects.select_related("product", "created_by", "supplier")[:80]
    return render(request, "stock/movements.html", {"movements": movements})


@login_required
def low_stock(request):
    return render(request, "stock/low_stock.html", {"products": generate_low_stock_report()})
