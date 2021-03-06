import random
import os
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from smart_selects.db_fields import ChainedForeignKey
from image_cropping.fields import ImageRatioField
from ecommerce.utils import unique_slug_generator
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    # print(instance)
    # print(filename)
    new_filename = random.randint(1, 33333333)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

class ProductQuerySet(models.query.QuerySet): #custom queryset
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self): #overrides Products.object.all()
        return self.get_queryset().active()

    def features(self):
        #return self.get_queryset().filter(featured=True)
        return self.get_queryset().featured() # instead of ^this line | from custom queryset

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('products:list_products_by_category', args=[self.slug])

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length = 400)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'

class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = ChainedForeignKey(
        Subcategory,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
        )
    price = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    cropping = ImageRatioField('image', '640x640')
    active =  models.BooleanField(default=True)
    inventory = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    size = models.CharField(max_length=30)
    weight = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    odor = models.CharField(max_length=50)

    def clean_inventory(self):
        if self.inventory < 0:
            raise ValidationError('Draft entries may not have a publication date.')
        return

    objects = ProductManager() # Product.objects.(something)

    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug": self.slug}) # app_name:name on urls.py

    def add_to_cart(self):
        return "{0}?item={1}&qty=1".format(reverse("carts:cart"), self.id) # string manipulation

    def remove_from_cart(self, instance):
        instance.cart.update_subtotal()
        return "{0}?item={1}&qty=1&delete=True".format(reverse("carts:cart"), self.id) # string manipulation

    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.title

# Slug generators
def product_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_reciever, sender=Product)

def category_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(category_pre_save_reciever, sender=Category)

def subcategory_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(subcategory_pre_save_reciever, sender=Subcategory)