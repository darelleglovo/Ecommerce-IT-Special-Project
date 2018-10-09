from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from .models import AboutUs, ContactUs

admin.site.register(AboutUs, SingleModelAdmin)
admin.site.register(ContactUs, SingleModelAdmin)