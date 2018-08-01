from django.contrib import admin
from .models import Product, Category, Subcategory

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'category']
    class Meta:
        model = Product
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'category']
    class Meta:
        model = Subcategory

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Subcategory, SubcategoryAdmin)