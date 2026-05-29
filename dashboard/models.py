from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=120)
    table_affected = models.CharField(max_length=120)
    record_id = models.CharField(max_length=80, blank=True)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["action", "created_at"])]

    def __str__(self):
        return f"{self.action} on {self.table_affected}"


class BusinessSettings(models.Model):
    business_name = models.CharField(max_length=160, default="DM Inventory")
    receipt_footer = models.CharField(max_length=180, default="Thank you for shopping with us.")
    allow_owner_stock_override = models.BooleanField(default=False)
    update_latest_cost_on_stock_in = models.BooleanField(default=True)
    currency_symbol = models.CharField(max_length=8, default="PHP")

    class Meta:
        verbose_name_plural = "business settings"

    def __str__(self):
        return self.business_name
