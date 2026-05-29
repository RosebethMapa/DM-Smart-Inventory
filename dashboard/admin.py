from django.contrib import admin

from .models import AuditLog, BusinessSettings


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("action", "table_affected", "record_id", "user", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("action", "table_affected", "record_id")


admin.site.register(BusinessSettings)
