from django.shortcuts import render
from django.http import Http404


def index(request):
    raise Http404("This page does not exist")


def custom_404(request, exception):
    return render(request, '404.html', status=404)
