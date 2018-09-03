# Django 2.0
from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page),
    path('register/', views.register_page, name='register'),
]