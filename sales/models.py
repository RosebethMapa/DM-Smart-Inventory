from decimal import Decimal

from django.conf import settings
from django.db import models


class Sale(models.Model):
    PAYMENT_CHOICES = [
        ("cash", "Cash"),
        ("gcash", "GCash"),
        ("bank", "Bank transfer"),
        ("credit", "Credit"),
    ]
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sales")
    customer_name = models.CharField(max_length=160, blank=True)
    customer_contact = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_PAID)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    profit = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default="cash")
    amount_received = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    change = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    balance_due = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    stock_committed = models.BooleanField(default=True)
    is_void = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["created_at", "is_void"]), models.Index(fields=["status", "created_at"])]

    def __str__(self):
        return f"Sale #{self.pk}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_sale = models.DecimalField(max_digits=12, decimal_places=2)
    cost_at_sale = models.DecimalField(max_digits=12, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)
    line_profit = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product}"


class Payment(models.Model):
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE, related_name="payment")
    method = models.CharField(max_length=30, choices=Sale.PAYMENT_CHOICES)
    amount_received = models.DecimalField(max_digits=12, decimal_places=2)
    change = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
