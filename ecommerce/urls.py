from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home_page),
    path('about/', views.about_page),
    path('contact/', views.contact_page),
    path('login/', views.login_page),
    path('admin/', admin.site.urls),
]
