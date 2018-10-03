# Django 2.0
from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('payment-confirmation/', views.upload_payment_proof, name='upload-payment-proof'),
    path('inquiry/success', views.upload_done, name='success'),
    path('myorders/', views.past_orders, name='past-orders'),
]