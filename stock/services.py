from django.db import transaction

from dashboard.models import AuditLog, BusinessSettings
from products.models import Product

from .models import StockMovement


@transaction.atomic
def add_stock(*, product, quantity, supplier=None, cost_per_unit=None, reference="", notes="", user=None):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    product = Product.objects.select_for_update().get(pk=product.pk)
    stock_before = product.current_stock
    product.current_stock += quantity
    settings = BusinessSettings.objects.first()
    if cost_per_unit is not None and (settings is None or settings.update_latest_cost_on_stock_in):
        product.cost_price = cost_per_unit
    product.save(update_fields=["current_stock", "cost_price", "updated_at"])

    movement = StockMovement.objects.create(
        product=product,
        movement_type=StockMovement.STOCK_IN,
        quantity=quantity,
        stock_before=stock_before,
        stock_after=product.current_stock,
        unit_cost=cost_per_unit,
        reference=reference,
        supplier=supplier or product.supplier,
        notes=notes,
        created_by=user,
    )
    AuditLog.objects.create(user=user, action="stock_in", table_affected="stock_movements", record_id=str(movement.pk))
    return movement


@transaction.atomic
def adjust_stock(*, product, adjustment_type, quantity, reason, notes="", user=None):
    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    product = Product.objects.select_for_update().get(pk=product.pk)
    stock_before = product.current_stock
    if adjustment_type == "add":
        product.current_stock += quantity
        movement_type = StockMovement.ADJUSTMENT_ADD
        movement_qty = quantity
    elif adjustment_type == "subtract":
        if quantity > product.current_stock:
            raise ValueError("Adjustment cannot make stock negative.")
        product.current_stock -= quantity
        movement_type = StockMovement.ADJUSTMENT_SUBTRACT
        movement_qty = -quantity
    elif adjustment_type == "set":
        product.current_stock = quantity
        movement_type = StockMovement.ADJUSTMENT_SET
        movement_qty = product.current_stock - stock_before
    else:
        raise ValueError("Invalid adjustment type.")

    product.save(update_fields=["current_stock", "updated_at"])
    movement = StockMovement.objects.create(
        product=product,
        movement_type=movement_type,
        quantity=movement_qty,
        stock_before=stock_before,
        stock_after=product.current_stock,
        reference=reason,
        notes=notes,
        created_by=user,
    )
    AuditLog.objects.create(user=user, action="stock_adjustment", table_affected="stock_movements", record_id=str(movement.pk))
    return movement
