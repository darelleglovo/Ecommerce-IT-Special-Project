from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include # Django 2.0
from django.contrib.auth import views as auth_views
from . import views
from accounts.views import login_page

urlpatterns = [
    path('', views.home_page),
    path('login/', login_page, name='login'),
    path('about/', views.about_page),
    path('contact/', views.contact_page),
    path('', include('accounts.urls')),
    path('', include('carts.urls')),
    path('', include('addresses.urls')),
    path('', include('billing.urls')),
    path('', include('orders.urls')),
    path('redirect/', views.registered, name='registered'),
    path('', include('products.urls')), # Django 2.0
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
admin.site.site_header = "Enghel's Collection Admin"
admin.site.site_title = "Enghel's Collection Admin"
admin.site.index_title = "Welcome to Einghel's Collection"
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)