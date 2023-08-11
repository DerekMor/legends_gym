from django.shortcuts import render

from .forms import CheckoutForm
from profiles.models import UserProfile  # Import your UserProfile model


def checkout(request):
    user = request.user
    initial_data = {}

    if user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=user)
            initial_data = {
                'full_name': profile.default_full_name,
                'email': profile.default_email,
                'phone_number': profile.default_phone_number,
                'street_address1': profile.default_street_address1,
                'street_address2': profile.default_street_address2,
                'town_or_city': profile.default_town_or_city,
                'county': profile.default_county,
                'country': profile.default_country,
                'postcode': profile.default_postcode,
            }
        except UserProfile.DoesNotExist:
            pass

    if request.method == 'POST':
        form = CheckoutForm(request.POST, initial=initial_data)
        if form.is_valid():

    else:
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
    }
    return render(request, 'checkout/checkout.html', context)
