from django import forms

from .models import Category, Product, Supplier


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name", "sku", "barcode", "category", "supplier", "cost_price", "selling_price",
            "current_stock", "reorder_level", "reorder_quantity", "unit_type", "image", "image_url", "is_active",
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "contact_person", "phone", "email", "address", "is_active"]
