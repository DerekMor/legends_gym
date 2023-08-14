from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CheckoutForm
from profiles.models import Customer
from .models import Order
from products.models import Product
from cart.contexts import cart_total
import stripe
from django.conf import settings


def checkout(request):
    user = request.user
    initial_data = {}
    cart_items = {}
    cart_total = 0
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get('cart', {})
    cart_items = {int(product_id): quantity for product_id,
                  quantity in cart_items.items()}
    if 'cart' in request.session:
        cart_items = request.session['cart']
        print("Cart Items:", cart_items)

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        cart_total += subtotal

    if request.method == 'POST':
        form = CheckoutForm(request.POST, initial=initial_data)
        if form.is_valid():
            order = form.save(commit=False)

            if user.is_authenticated:

                customer = Customer.objects.get(user=user)
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

    print("stripe_public_key:", stripe_public_key)

    print("stripe_secret_key:", stripe_secret_key)

    stripe_total = round(cart_total * 100)

    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    print(intent)

    context = {
        'form': form,
        'cart_items': list(cart_items.values()),
        'cart_total': cart_total,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):

    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
