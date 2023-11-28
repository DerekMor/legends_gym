# from .webhooks import webhooks
from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>',
         views.checkout_success, name='checkout_success'),
    path('generate-one-time-code/', views.generate_one_time_code, name='generate_one_time_code'),
]
