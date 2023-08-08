from products.models import Product
from django.shortcuts import render


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []

    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append(
            {'product': product, 'quantity': quantity, 'subtotal': subtotal})

    context = {
        'cart_items': cart_items,
        'cart_total': total,
    }

    return render(request, 'cart/cart.html', context)
