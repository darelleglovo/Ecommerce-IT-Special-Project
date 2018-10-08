# Django 2.0
from django.urls import path, include
from . import views

app_name = 'search'
urlpatterns = [
    path('search/', views.SearchProductView.as_view(), name='query'),
]