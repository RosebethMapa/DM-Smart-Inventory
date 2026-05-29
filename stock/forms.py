from django import forms

from products.models import Product, Supplier


class StockInForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_active=True).select_related("supplier"))
    quantity = forms.IntegerField(min_value=1)
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.filter(is_active=True), required=False)
    cost_per_unit = forms.DecimalField(min_value=0, max_digits=12, decimal_places=2)
    reference = forms.CharField(max_length=120, required=False)
    notes = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)


class StockAdjustmentForm(forms.Form):
    ADJUSTMENT_CHOICES = [("add", "Add"), ("subtract", "Subtract"), ("set", "Set exact count")]

    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_active=True))
    adjustment_type = forms.ChoiceField(choices=ADJUSTMENT_CHOICES)
    quantity = forms.IntegerField(min_value=0)
    reason = forms.CharField(max_length=120)
    notes = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)
