from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include # Django 2.0
from . import views

urlpatterns = [
    path('', views.home_page),
    path('about/', views.about_page),
    path('contact/', views.contact_page),
    path('login/', views.login_page),
    path('', include('products.urls')), # Django 2.0
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)