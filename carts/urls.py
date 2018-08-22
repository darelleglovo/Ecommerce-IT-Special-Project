# Django 2.0
from django.urls import path, include
from . import views

app_name = 'carts'
urlpatterns = [
    path('cart/', views.cart_home, name='home'),
    path('cart/update/', views.cart_update, name='update'),
]