# Django 2.0
from django.urls import path, include
from . import views

app_name = 'billing'
urlpatterns = [
    path('billing/payment-method/', views.payment_method_view, name='billing-payment-method'),
    path('billing/payment-method/create', views.payment_method_createview, name='billing-payment-method-endpoint'),
    path('payment-confirmation/', views.upload_payment_proof, name='upload-payment-proof'),

]