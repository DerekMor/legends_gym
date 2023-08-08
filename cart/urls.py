
from django.contrib import admin
from django.urls import path
from . import views
from .views import add_to_cart


urlpatterns = [
    path('', views.view_cart, name="view_cart"),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

]
