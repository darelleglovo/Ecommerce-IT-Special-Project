from django.contrib import admin
from .models import Product, Category, Subcategory
from social_django.models import Association, Nonce, UserSocialAuth
from django.contrib.auth.models import Group
from image_cropping import ImageCroppingMixin




def make_active(modeladmin, request, queryset):
    queryset.update(active=True)

def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)


make_active.short_description = "Mark selected product as active"
make_inactive.short_description = "Mark selected product as inactive"

class ProductAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ['__str__', 'category', 'subcategory', 'active', 'inventory']
    list_filter = ['category']
    search_fields = ['title']
    actions = [make_active, make_inactive]
    class Meta:
        model = Product
        verbose_name = 'asd'
        verbose_name_plural = 'asdasdasd'

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

admin.site.unregister(Group)
admin.site.unregister(Association)
admin.site.unregister(Nonce)
#admin.site.unregister(Group)