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
            name="StockMovement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("movement_type", models.CharField(choices=[("stock_in", "Stock in"), ("sale", "Sale"), ("adjustment_add", "Adjustment add"), ("adjustment_subtract", "Adjustment subtract"), ("adjustment_set", "Adjustment set"), ("void_sale", "Void sale")], max_length=40)),
                ("quantity", models.IntegerField()),
                ("stock_before", models.IntegerField()),
                ("stock_after", models.IntegerField()),
                ("unit_cost", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ("reference", models.CharField(blank=True, max_length=120)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="movements", to="products.product")),
                ("supplier", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="products.supplier")),
            ],
            options={"ordering": ["-created_at"], "indexes": [models.Index(fields=["movement_type", "created_at"], name="stock_stock_movemen_1fc8bb_idx"), models.Index(fields=["product", "created_at"], name="stock_stock_product_f976cb_idx")]},
        ),
    ]
