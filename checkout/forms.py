from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number', 'country', 'postcode',
                  'town_or_city', 'street_address1', 'street_address2', 'county']


class DiscountCodeForm(forms.Form):
    code = forms.CharField(max_length=20)
