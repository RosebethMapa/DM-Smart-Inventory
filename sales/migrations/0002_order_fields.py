from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sales", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sale",
            name="customer_contact",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="sale",
            name="customer_name",
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name="sale",
            name="status",
            field=models.CharField(choices=[("pending", "Pending"), ("paid", "Paid"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="paid", max_length=30),
        ),
        migrations.AddField(
            model_name="sale",
            name="stock_committed",
            field=models.BooleanField(default=True),
        ),
        migrations.AddIndex(
            model_name="sale",
            index=models.Index(fields=["status", "created_at"], name="sales_sale_status_44e2bc_idx"),
        ),
    ]
