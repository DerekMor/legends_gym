
from django.contrib import admin
from django.urls import path
from . import views
from .views import add_to_cart, remove_from_cart, update_cart



urlpatterns = [
    path('', views.view_cart, name="view_cart"),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/',
         remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:product_id>/',
         update_cart, name='update_cart'),
     path('apply_discount_code/', views.apply_discount_code, name='apply_discount_code'),

]
