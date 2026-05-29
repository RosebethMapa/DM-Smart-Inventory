from decimal import Decimal

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Sale",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("subtotal", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12)),
                ("discount", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12)),
                ("total_amount", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12)),
                ("total_cost", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12)),
                ("profit", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12)),
                ("payment_method", models.CharField(choices=[("cash", "Cash"), ("gcash", "GCash"), ("bank", "Bank transfer"), ("credit", "Credit")], default="cash", max_length=30)),
                ("amount_received", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12)),
                ("change", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12)),
                ("balance_due", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12)),
                ("is_void", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("cashier", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="sales", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"], "indexes": [models.Index(fields=["created_at", "is_void"], name="sales_sale_created_1b65f1_idx")]},
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("method", models.CharField(choices=[("cash", "Cash"), ("gcash", "GCash"), ("bank", "Bank transfer"), ("credit", "Credit")], max_length=30)),
                ("amount_received", models.DecimalField(decimal_places=2, max_digits=12)),
                ("change", models.DecimalField(decimal_places=2, max_digits=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("sale", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="payment", to="sales.sale")),
            ],
        ),
        migrations.CreateModel(
            name="SaleItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField()),
                ("price_at_sale", models.DecimalField(decimal_places=2, max_digits=12)),
                ("cost_at_sale", models.DecimalField(decimal_places=2, max_digits=12)),
                ("line_total", models.DecimalField(decimal_places=2, max_digits=12)),
                ("line_profit", models.DecimalField(decimal_places=2, max_digits=12)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="products.product")),
                ("sale", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="sales.sale")),
            ],
        ),
    ]
