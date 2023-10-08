from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review
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


def single_product(request, pk):

    product = get_object_or_404(Product, pk=pk)

    context = {
        'product': product,
    }

    return render(request, 'products/single_product.html', context)


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