from decimal import Decimal

from django.db import transaction

from dashboard.models import AuditLog
from products.models import Product
from stock.models import StockMovement

from .models import Payment, Sale, SaleItem
from .notifications import notify_order_success


def _prepare_order_items(items):
    if not items:
        raise ValueError("Cart is empty.")
    locked_products = {
        product.pk: product
        for product in Product.objects.select_for_update().filter(pk__in=[item["product"].pk for item in items], is_active=True)
    }
    subtotal = Decimal("0.00")
    total_cost = Decimal("0.00")
    prepared_items = []

    for item in items:
        product = locked_products.get(item["product"].pk)
        quantity = int(item["quantity"])
        if not product:
            raise ValueError("One product in the cart is unavailable.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if quantity > product.current_stock:
            raise ValueError(f"Not enough stock for {product.name}. Available: {product.current_stock}.")

        line_total = product.selling_price * quantity
        line_cost = product.cost_price * quantity
        subtotal += line_total
        total_cost += line_cost
        prepared_items.append((product, quantity, line_total, line_cost))
    return subtotal, total_cost, prepared_items


def _payment_totals(*, subtotal, total_cost, payment_method, amount_received, discount):
    if discount < 0:
        raise ValueError("Discount cannot be negative.")

    total_amount = max(Decimal("0.00"), subtotal - discount)
    amount_received = Decimal(amount_received)
    change = max(Decimal("0.00"), amount_received - total_amount) if payment_method == "cash" else Decimal("0.00")
    balance_due = max(Decimal("0.00"), total_amount - amount_received)
    profit = total_amount - total_cost
    return total_amount, amount_received, change, balance_due, profit


@transaction.atomic
def create_sale(
    *,
    cashier,
    items,
    payment_method,
    amount_received,
    discount=Decimal("0.00"),
    customer_name="",
    customer_contact="",
    status=Sale.STATUS_PAID,
):
    subtotal, total_cost, prepared_items = _prepare_order_items(items)
    total_amount, amount_received, change, balance_due, profit = _payment_totals(
        subtotal=subtotal,
        total_cost=total_cost,
        payment_method=payment_method,
        amount_received=amount_received,
        discount=discount,
    )
    should_commit_stock = status in [Sale.STATUS_PAID, Sale.STATUS_COMPLETED]

    sale = Sale.objects.create(
        cashier=cashier,
        customer_name=customer_name,
        customer_contact=customer_contact,
        status=status,
        subtotal=subtotal,
        discount=discount,
        total_amount=total_amount,
        total_cost=total_cost,
        profit=profit,
        payment_method=payment_method,
        amount_received=amount_received,
        change=change,
        balance_due=balance_due,
        stock_committed=should_commit_stock,
    )

    for product, quantity, line_total, line_cost in prepared_items:
        stock_before = product.current_stock
        if should_commit_stock:
            product.current_stock -= quantity
            product.save(update_fields=["current_stock", "updated_at"])
        SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=quantity,
            price_at_sale=product.selling_price,
            cost_at_sale=product.cost_price,
            line_total=line_total,
            line_profit=line_total - line_cost,
        )
        if should_commit_stock:
            StockMovement.objects.create(
                product=product,
                movement_type=StockMovement.SALE,
                quantity=-quantity,
                stock_before=stock_before,
                stock_after=product.current_stock,
                reference=f"Order #{sale.pk}",
                created_by=cashier,
            )

    if status != Sale.STATUS_PENDING:
        Payment.objects.create(sale=sale, method=payment_method, amount_received=amount_received, change=change)
    AuditLog.objects.create(user=cashier, action=f"order_{status}", table_affected="sales", record_id=str(sale.pk))
    transaction.on_commit(lambda sale_id=sale.pk: notify_order_success(sale_id))
    return sale


@transaction.atomic
def update_order_status(*, sale, status, user=None):
    sale = Sale.objects.select_for_update().get(pk=sale.pk)
    if sale.status == Sale.STATUS_CANCELLED:
        raise ValueError("Cancelled orders cannot be updated.")
    if status == Sale.STATUS_CANCELLED:
        sale.status = status
        sale.is_void = True
        sale.save(update_fields=["status", "is_void"])
        AuditLog.objects.create(user=user, action="order_cancelled", table_affected="sales", record_id=str(sale.pk))
        return sale
    if status not in [Sale.STATUS_PAID, Sale.STATUS_COMPLETED]:
        raise ValueError("Invalid order status.")
    if not sale.stock_committed:
        for item in sale.items.select_related("product"):
            product = Product.objects.select_for_update().get(pk=item.product.pk)
            if item.quantity > product.current_stock:
                raise ValueError(f"Not enough stock for {product.name}. Available: {product.current_stock}.")
            stock_before = product.current_stock
            product.current_stock -= item.quantity
            product.save(update_fields=["current_stock", "updated_at"])
            StockMovement.objects.create(
                product=product,
                movement_type=StockMovement.SALE,
                quantity=-item.quantity,
                stock_before=stock_before,
                stock_after=product.current_stock,
                reference=f"Order #{sale.pk}",
                created_by=user,
            )
        sale.stock_committed = True
    sale.status = status
    sale.save(update_fields=["status", "stock_committed"])
    if not hasattr(sale, "payment") and status in [Sale.STATUS_PAID, Sale.STATUS_COMPLETED]:
        Payment.objects.create(sale=sale, method=sale.payment_method, amount_received=sale.amount_received, change=sale.change)
    AuditLog.objects.create(user=user, action=f"order_{status}", table_affected="sales", record_id=str(sale.pk))
    return sale
