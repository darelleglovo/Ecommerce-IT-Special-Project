from django.contrib import admin
from .models import Product, Category, SubCategory

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'category']
    class Meta:
        model = Product
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(SubCategory)