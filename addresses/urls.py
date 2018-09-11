# Django 2.0
from django.urls import path, include
from . import views

app_name = 'addresses'
urlpatterns = [
    path('checkout/address/create/', views.checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', views.checkout_address_reuse_view, name='checkout_address_reuse'),

]