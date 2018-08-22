from django.contrib import admin
from .models import Product, Category, Subcategory
from social_django.models import Association, Nonce, UserSocialAuth
from django.contrib.auth.models import Group
from image_cropping import ImageCroppingMixin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group, User

from .models import Role


admin.site.unregister(Group)

# admin.site.register(Role, GroupAdmin)

class UserAdmin(admin.ModelAdmin):
    exclude = ['groups']

class ProductAdmin(ImageCroppingMixin, admin.ModelAdmin):
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
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

admin.site.unregister(Association)
admin.site.unregister(Nonce)
#admin.site.unregister(Group)