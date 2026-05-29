from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="BusinessSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("business_name", models.CharField(default="Smart Inventory Store", max_length=160)),
                ("receipt_footer", models.CharField(default="Thank you for shopping with us.", max_length=180)),
                ("allow_owner_stock_override", models.BooleanField(default=False)),
                ("update_latest_cost_on_stock_in", models.BooleanField(default=True)),
                ("currency_symbol", models.CharField(default="PHP", max_length=8)),
            ],
            options={"verbose_name_plural": "business settings"},
        ),
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("action", models.CharField(max_length=120)),
                ("table_affected", models.CharField(max_length=120)),
                ("record_id", models.CharField(blank=True, max_length=80)),
                ("old_value", models.JSONField(blank=True, null=True)),
                ("new_value", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"], "indexes": [models.Index(fields=["action", "created_at"], name="dashboard_a_action_9e6d90_idx")]},
        ),
    ]
