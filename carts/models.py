from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from decimal import Decimal
# Create your models here.

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.DO_NOTHING)
    item = models.ForeignKey('products.Product', on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.item.title
    def __unicode__(self):
        return self.item.title
    def get_absolute_url(self):
        return self.item.get_absolute_url()
    def remove(self):
        return self.item.remove_from_cart(instance=self)
        #return "%s?item=%s&delete=True" %(reverse("carts:cart"), self.item.id) # string manipulation

def cart_item_pre_save_reciever(sender, instance, *args, **kwargs):
    qty = instance.quantity
    if qty >= 1:
        price = instance.item.price
        line_item_total = Decimal(qty) * Decimal(price)
        instance.line_item_total = line_item_total

pre_save.connect(cart_item_pre_save_reciever,sender=CartItem)

def cart_item_post_save_reciever(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()

post_save.connect(cart_item_post_save_reciever, sender=CartItem)

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.DO_NOTHING)
    items = models.ManyToManyField('products.Product', through=CartItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    subtotal = models.DecimalField(max_digits=50, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=50, decimal_places=2, null=True)

    def __str__(self):
        return str(self.id)
    def __unicode__(self):
        return str(self.id)
    def update_subtotal(self):
        subtotal = 0;
        items = self.cartitem_set.all()
        for item in items:
            subtotal += item.line_item_total
        self.subtotal = subtotal
        self.save()

def do_total_reciever(sender, instance, *args, **kwargs):
    try:
        subtotal = instance.subtotal
        total = subtotal + 10
        instance.total = total
    except:
        pass

pre_save.connect(do_total_reciever, sender=Cart)





