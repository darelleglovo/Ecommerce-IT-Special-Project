# Django 2.0
from django.urls import path, include
from . import views

app_name = 'cms'
urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact-us/', views.contact, name='contact'),
]