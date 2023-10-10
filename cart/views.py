from products.models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from checkout.forms import DiscountCodeForm
from checkout.models import DiscountCode


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []

    cart_total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        cart_total += subtotal
        cart_items.append(
            {'product': product, 'quantity': quantity, 'subtotal': subtotal})

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }

    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    request.session['cart'] = cart
    print('debug. ID:', product_id)
    messages.success(
        request, f"{quantity} {product.name}{'s' if quantity > 1 else ''} added to your cart.")
    return redirect('products')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    str_product_id = str(product_id)

    if str_product_id in cart:
        del cart[str_product_id]
        request.session['cart'] = cart
        request.session.save()
        messages.success(request, "Item removed from your cart.")
    else:
        
        messages.error(request, "Item not found in your cart.")

    return redirect('view_cart')


def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart = request.session.get('cart', {})
            cart[product_id] = quantity
            request.session['cart'] = cart

    return redirect('view_cart')


def apply_discount_code(request):
    if request.method == 'POST':
        discount_code_form = DiscountCodeForm(request.POST)
        if discount_code_form.is_valid():
            discount_code = discount_code_form.cleaned_data['code']
            
            try:
                discount = DiscountCode.objects.get(code=discount_code, used=False)

                if discount.percentage > 0:
                    cart_total = request.session.get('cart_total', 0)
                    discount_amount = (discount.percentage / 100) * cart_total
                    cart_total -= float(discount_amount)  # Convert to float

                    discount.used = True
                    discount.save()

                    request.session['cart_total'] = cart_total

                    messages.success(request, 'Discount code applied successfully.')
                else:
                    messages.error(request, 'Invalid discount code.')
            except DiscountCode.DoesNotExist:
                messages.error(request, 'Discount code not found or already used.')
        else:
            messages.error(request, 'Invalid discount code.')
    else:
        messages.error(request, 'Invalid request.')

    return redirect('view_cart')
