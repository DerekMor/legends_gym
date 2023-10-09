from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, Wishlist
from django.contrib.auth.decorators import login_required


def all_products(request):

    products = Product.objects.all()
    query = None
    category_filter = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'No search term was provided!')
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            products = products.filter(queries)

        if 'category' in request.GET:
            category_filter = request.GET['category']
            if category_filter:
                products = products.filter(category__name=category_filter)

            if category_filter == 'plans':
                products = products.exclude(category__name='plans')

        sort_by = request.GET.get('sort', 'name')
        direction = request.GET.get('direction', 'asc')

        if direction == 'asc':
            sort_by = sort_by
        elif direction == 'desc':
            sort_by = f'-{sort_by}'

        products = products.order_by(sort_by)

    context = {
        'products': products,
        'search_term': query,
        'category_filter': category_filter,
    }

    return render(request, 'products/products.html', context)


def single_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    wishlist, created = Wishlist.objects.get_or_create(user=user)

    if request.method == 'POST':
        if 'add_to_wishlist' in request.POST:
            if product in wishlist.products.all():
                messages.warning(request, 'This item is already in your wishlist.')
            else:
                wishlist.products.add(product)
                messages.success(request, 'Item added to your wishlist successfully.')
        elif 'remove_from_wishlist' in request.POST:
            if product in wishlist.products.all():
                wishlist.products.remove(product)
                messages.success(request, 'Item removed from your wishlist successfully.')
            else:
                messages.warning(request, 'This item is not in your wishlist.')

    return render(request, 'single_product.html', {'product': product, 'wishlist': wishlist})



def plans_products(request):
    plans_products = Product.objects.filter(category__name='plans')

    context = {
        'products': plans_products,
        'category_filter': 'plans',
    }

    return render(request, 'products/products.html', context)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        rating = request.POST['rating']
        user = request.user

        
        existing_review = Review.objects.filter(user=user, product=product).first()

        if existing_review:
            existing_review.title = title
            existing_review.content = content
            existing_review.rating = rating
            existing_review.save()
        else:
            Review.objects.create(user=user, product=product, title=title, content=content, rating=rating)

        return redirect('single_product', pk=product_id)

    return render(request, 'products/add_review.html', {'product': product})

@login_required
def delete_review(request, product_id, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if review.user == request.user:
        review.delete()

    return redirect('single_product', pk=review.product.id)


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    wishlist, created = Wishlist.objects.get_or_create(user=user)

    if wishlist.products.filter(pk=product_id).exists():
        messages.warning(request, 'This item is already in your wishlist.')
    else:
        wishlist.products.add(product)
        messages.success(request, 'Item added to your wishlist successfully.')

    return redirect('single_product', product_id=product_id)


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    wishlist, created = Wishlist.objects.get_or_create(user=user)

    if wishlist.products.filter(pk=product_id).exists():
        wishlist.products.remove(product)
        messages.success(request, 'Item removed from your wishlist successfully.')
    else:
        messages.warning(request, 'This item is not in your wishlist.')

    return redirect('single_product', product_id=product_id)