from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CheckoutForm, DiscountCodeForm
from profiles.models import Customer
from .models import Order, OrderLineItem, DiscountCode
from products.models import Product
from cart.contexts import cart_total
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
import uuid

@login_required
def checkout(request):
    print("Entering checkout view")
    user = request.user
    initial_data = {}
    cart_items = {}
    cart_total = 0
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    discount_code_form = DiscountCodeForm()

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
        print("Processing POST request")
        form = CheckoutForm(request.POST, initial=initial_data)
        if form.is_valid():
            order = form.save(commit=False)

            if user.is_authenticated:

                try:
                    order = form.save(commit=False)
                    customer = Customer.objects.get(user=user)
                    order.customer = customer
                    order.order_total = cart_total
                    order.save()

                    for product_id, quantity in cart.items():
                        product = get_object_or_404(Product, id=product_id)
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            lineitem_total=product.price * quantity
                        )

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

                except Customer.DoesNotExist:
                    print('user does not exist')

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
                order.save()  
                return checkout_success(request, order.order_number)
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
        'client_secret': intent.client_secret,
        'discount_code_form': discount_code_form,
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

@login_required
@permission_required('checkout.can_generate_discount_code', raise_exception=True)
def generate_one_time_code(request):
    if request.method == 'POST':
        try:
        
            percentage = float(request.POST['percentage'])
            if 0 <= percentage <= 100:
                one_time_code = "SOME_UNIQUE_CODE"
                discount_code = DiscountCode.objects.create(
                    code=one_time_code, percentage=percentage)
                OneTimeDiscountCode.objects.create(discount_code=discount_code)

                messages.success(
                    request, 'One-time discount code generated successfully.')
                return redirect('generate_one_time_code')
            else:
                messages.error(request, 'Invalid percentage value.')
        except ValueError:
            messages.error(request, 'Invalid percentage format.')
    
    return render(request, 'checkout/generate_one_time_code.html')