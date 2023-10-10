from products.models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from checkout.forms import DiscountCodeForm
from checkout.models import DiscountCode
from decimal import Decimal


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []

    cart_total = Decimal('0.00')

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        cart_total += subtotal
        cart_items.append(
            {'product': product, 'quantity': quantity, 'subtotal': subtotal})

    discount_amount = Decimal(str(request.session.get('discount_amount', 0.00)))
    cart_total -= discount_amount

    request.session['cart_total'] = float(cart_total)

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
                    cart_total = request.session.get('cart_total', Decimal('0.00'))
                    print('before', cart_total)
                    cart_total_decimal = Decimal(str(cart_total))
                    discount_percentage = Decimal(str(discount.percentage))
                    discount_amount = (discount_percentage / Decimal('100.00')) * cart_total_decimal
                    request.session['discount_amount'] = float(discount_amount)
                    cart_total_decimal -= discount_amount

                    print('Cart Total After Applying Discount:', cart_total_decimal)
                    print('Discount Amount:', discount_amount)

                    discount.used = True
                    discount.save()

                    cart_total_decimal = float(cart_total_decimal)
                    request.session['cart_total'] = cart_total_decimal

                    print('Updated Cart Total:', cart_total_decimal)

                    messages.success(request, 'Discount code applied successfully.')
                    request.session.save()
                else:
                    messages.error(request, 'Invalid discount code.')
            except DiscountCode.DoesNotExist:
                messages.error(request, 'Discount code not found or already used.')
        else:
            messages.error(request, 'Invalid discount code form.')
    else:
        messages.error(request, 'Invalid request.')

    return redirect('view_cart')