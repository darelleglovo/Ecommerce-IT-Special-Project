from django.contrib import admin
from .models import Product, Category, Subcategory
from social_django.models import Association, Nonce, UserSocialAuth



class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'category', 'subcategory', 'slug']
    list_filter = ['category']
    class Meta:
        model = Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    class Meta:
        model = Category

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'category', 'slug']
    list_filter = ['category']
    class Meta:
        model = Subcategory

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)

admin.site.unregister(Association)
admin.site.unregister(Nonce)