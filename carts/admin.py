from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem

class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartItemInline
    ]
    readonly_fields = ('timestamp',)
    list_display = ['__str__', 'is_done']
    class Meta:
        model = Cart

#admin.site.register(Cart, CartAdmin)
#admin.site.register(CartItem)