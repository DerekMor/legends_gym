from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CheckoutForm
from profiles.models import Customer
from .models import Order
from products.models import Product


def checkout(request):
    user = request.user
    initial_data = {}
    cart_items = {}
    cart_total = 0

    cart = request.session.get('cart', {})
    cart_items = {int(product_id): quantity for product_id,
                  quantity in cart_items.items()}
    if 'cart' in request.session:
        cart_items = request.session['cart']
        print("Cart Items:", cart_items)

    if user.is_authenticated:
        try:
            customer = Customer.objects.get(user=user)
            initial_data = {
                'full_name': customer.default_full_name,
                'email': customer.default_email,
                'phone_number': customer.default_phone_number,
                'street_address1': customer.default_street_address1,
                'street_address2': customer.default_street_address2,
                'town_or_city': customer.default_town_or_city,
                'county': customer.default_county,
                'country': customer.default_country,
                'postcode': customer.default_postcode,
            }
        except Customer.DoesNotExist:
            pass

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        cart_total += subtotal

    if request.method == 'POST':
        form = CheckoutForm(request.POST, initial=initial_data)
        if form.is_valid():
            order = form.save(commit=False)

            if user.is_authenticated:

                order.customer = customer
                order.save()

                customer.default_full_name = form.cleaned_data['full_name']
                customer.default_email = form.cleaned_data['email']
                customer.default_phone_number = form.cleaned_data['phone_number']
                customer.default_street_address1 = form.cleaned_data['street_address1']
                customer.default_street_address2 = form.cleaned_data['street_address2']
                customer.default_town_or_city = form.cleaned_data['town_or_city']
                customer.default_county = form.cleaned_data['county']
                customer.default_country = form.cleaned_data['country']
                customer.default_postcode = form.cleaned_data['postcode']
                customer.save()

                if form.cleaned_data.get('save_info'):
                    customer.default_full_name = form.cleaned_data['full_name']
                    customer.default_email = form.cleaned_data['email']
                    customer.default_phone_number = form.cleaned_data['phone_number']
                    customer.default_street_address1 = form.cleaned_data['street_address1']
                    customer.default_street_address2 = form.cleaned_data['street_address2']
                    customer.default_town_or_city = form.cleaned_data['town_or_city']
                    customer.default_county = form.cleaned_data['county']
                    customer.default_country = form.cleaned_data['country']
                    customer.default_postcode = form.cleaned_data['postcode']
                    customer.save()

                messages.success(request, 'Order successfully placed!')
                return redirect('home')
            else:
                messages.error(
                    request, 'You need to be logged in to place an order.')
        else:
            messages.error(
                request, 'There was an error with your form submission. Please correct the errors.')

    else:
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart_items': list(cart_items.values()),
        'cart_total': cart_total,
    }
    return render(request, 'checkout/checkout.html', context)
