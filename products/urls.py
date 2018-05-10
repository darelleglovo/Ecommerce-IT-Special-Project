# Django 2.0
from django.urls import path, include
from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view()),
    path('products-fbv/', views.product_list_view),
    path('products/<int:pk>/', views.ProductDetailView.as_view()),
    path('products-fbv/<int:pk>/', views.product_detail_view),
]