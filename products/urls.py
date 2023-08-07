from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name="products"),
    path('product/<int:pk>/', views.single_product, name='single_product'),

]
