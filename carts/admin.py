from django.contrib import admin

from .models import Cart
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    filter_horizontal = ('products',)
admin.site.register(Cart, CartAdmin)