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
    path('logout/', views.logout_page),
    path('', include('products.urls')), # Django 2.0
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
]
admin.site.site_header = "Enghel's Collection Admin"
admin.site.site_title = "Enghel's Collection Admin"
admin.site.index_title = "Welcome to Einghel's Collection"
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)