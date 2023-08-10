from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product


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
