from decimal import Decimal

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
            options={"verbose_name_plural": "categories", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Supplier",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160, unique=True)),
                ("contact_person", models.CharField(blank=True, max_length=120)),
                ("phone", models.CharField(blank=True, max_length=60)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("address", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=180)),
                ("sku", models.CharField(max_length=80, unique=True)),
                ("barcode", models.CharField(blank=True, db_index=True, max_length=120)),
                ("cost_price", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12)),
                ("selling_price", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12)),
                ("current_stock", models.IntegerField(default=0)),
                ("reorder_level", models.PositiveIntegerField(default=5)),
                ("reorder_quantity", models.PositiveIntegerField(default=10)),
                ("unit_type", models.CharField(choices=[("piece", "Piece"), ("box", "Box"), ("kg", "Kg"), ("pack", "Pack"), ("bottle", "Bottle"), ("sachet", "Sachet")], default="piece", max_length=30)),
                ("image_url", models.URLField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="products.category")),
                ("supplier", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="products.supplier")),
            ],
            options={"ordering": ["name"], "indexes": [models.Index(fields=["name"], name="products_pr_name_8e1b52_idx"), models.Index(fields=["sku"], name="products_pr_sku_496f25_idx"), models.Index(fields=["is_active", "current_stock"], name="products_pr_is_acti_d9e966_idx")]},
        ),
    ]
