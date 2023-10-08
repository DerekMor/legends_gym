from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name="products"),
    path('product/<int:pk>/', views.single_product, name='single_product'),
    path('products/plans/', views.plans_products, name='plans_products'),
    path('products/<int:product_id>/add_review/', views.add_review, name='add_review'),
    path('products/<int:product_id>/delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
]
