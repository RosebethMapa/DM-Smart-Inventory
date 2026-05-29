from decimal import Decimal

from django import forms


class SaleForm(forms.Form):
    cart = forms.CharField(widget=forms.HiddenInput)
    customer_name = forms.CharField(max_length=160, required=False, widget=forms.TextInput(attrs={"placeholder": "Customer name"}))
    customer_contact = forms.CharField(max_length=80, required=False, widget=forms.TextInput(attrs={"placeholder": "Contact number"}))
    order_status = forms.ChoiceField(choices=[("pending", "Pending"), ("paid", "Paid"), ("completed", "Completed")], initial="paid")
    payment_method = forms.ChoiceField(choices=[("cash", "Cash"), ("gcash", "GCash"), ("bank", "Bank transfer"), ("credit", "Credit")])
    amount_received = forms.DecimalField(min_value=Decimal("0.00"), max_digits=12, decimal_places=2)
    discount = forms.DecimalField(min_value=Decimal("0.00"), max_digits=12, decimal_places=2, initial=Decimal("0.00"))


class CustomerOrderForm(forms.Form):
    cart = forms.CharField(widget=forms.HiddenInput)
    customer_name = forms.CharField(max_length=160, widget=forms.TextInput(attrs={"placeholder": "Your name"}))
    customer_contact = forms.CharField(
        max_length=80,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Contact number"}),
    )
