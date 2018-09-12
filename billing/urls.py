# Django 2.0
from django.urls import path, include
from . import views

app_name = 'billing'
urlpatterns = [
    path('billing/payment-method/', views.payment_method_view, name='billing-payment-method'),

]