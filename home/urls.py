
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),

]

handler404 = 'home.views.custom_404'
