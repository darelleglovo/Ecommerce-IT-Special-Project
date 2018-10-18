# Django 2.0
from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    #path('register/guest', views.guest_register_view, name='guest_register'),
    path('change-password/', views.change_password, name='change_password'),
    path('myaccount/', views.account_info, name='account_info'),
    path('profile/edit-email/', views.change_email, name='change_email'),
    path('profile/edit-address/', views.edit_address, name='edit_address'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),

]