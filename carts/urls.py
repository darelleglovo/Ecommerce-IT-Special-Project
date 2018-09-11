# Django 2.0
from django.urls import path, include
from . import views

app_name = 'carts'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/count/', views.ItemCountView.as_view(), name='item_count'),
    path('checkout/', views.checkout_home, name='checkout'),
    path('checkout/success/', views.chechout_done_view, name='success'),

]