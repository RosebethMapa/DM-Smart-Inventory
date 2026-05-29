from django.conf import settings
from django.db import models


class StockMovement(models.Model):
    STOCK_IN = "stock_in"
    SALE = "sale"
    ADJUSTMENT_ADD = "adjustment_add"
    ADJUSTMENT_SUBTRACT = "adjustment_subtract"
    ADJUSTMENT_SET = "adjustment_set"
    VOID_SALE = "void_sale"

    MOVEMENT_CHOICES = [
        (STOCK_IN, "Stock in"),
        (SALE, "Sale"),
        (ADJUSTMENT_ADD, "Adjustment add"),
        (ADJUSTMENT_SUBTRACT, "Adjustment subtract"),
        (ADJUSTMENT_SET, "Adjustment set"),
        (VOID_SALE, "Void sale"),
    ]

    product = models.ForeignKey("products.Product", on_delete=models.PROTECT, related_name="movements")
    movement_type = models.CharField(max_length=40, choices=MOVEMENT_CHOICES)
    quantity = models.IntegerField()
    stock_before = models.IntegerField()
    stock_after = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    reference = models.CharField(max_length=120, blank=True)
    supplier = models.ForeignKey("products.Supplier", on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["movement_type", "created_at"]),
            models.Index(fields=["product", "created_at"]),
        ]

    def __str__(self):
        return f"{self.product} {self.movement_type} {self.quantity}"
