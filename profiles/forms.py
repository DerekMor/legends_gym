from django import forms
from .models import Customer

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['default_phone_number', 'default_street_address1', 'default_street_address2', 'default_town_or_city', 'default_county', 'default_postcode', 'default_country', 'profile_picture']


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['profile_picture']