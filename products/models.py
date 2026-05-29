from decimal import Decimal

from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=160, unique=True)
    contact_person = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ("piece", "Piece"),
        ("box", "Box"),
        ("kg", "Kg"),
        ("pack", "Pack"),
        ("bottle", "Bottle"),
        ("sachet", "Sachet"),
    ]

    name = models.CharField(max_length=180)
    sku = models.CharField(max_length=80, unique=True)
    barcode = models.CharField(max_length=120, blank=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="products")
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    current_stock = models.IntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=5)
    reorder_quantity = models.PositiveIntegerField(default=10)
    unit_type = models.CharField(max_length=30, choices=UNIT_CHOICES, default="piece")
    image = models.FileField(upload_to="products/", blank=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["is_active", "current_stock"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_absolute_url(self):
        return reverse("product_list")

    @property
    def image_src(self):
        if self.image:
            return self.image.url
        return self.image_url

    @property
    def is_low_stock(self):
        return self.current_stock <= self.reorder_level

    @property
    def is_out_of_stock(self):
        return self.current_stock <= 0

    @property
    def stock_value(self):
        return self.current_stock * self.cost_price

    @property
    def potential_profit(self):
        return self.current_stock * (self.selling_price - self.cost_price)

    @property
    def suggested_reorder(self):
        return max(self.reorder_quantity, (self.reorder_level * 2) - self.current_stock)
