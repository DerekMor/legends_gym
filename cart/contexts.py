from django.shortcuts import get_object_or_404
from products.models import Product


def cart_total(request):
    cart = request.session.get('cart', {})
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
    return {'cart_total': total}
