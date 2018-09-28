import random
import os
from django.db import models
from django.db.models.signals import pre_save, post_save
import math

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.template import loader

from ecommerce.utils import unique_order_id_generator
from carts.models import Cart

from billing.models import BillingProfile
from addresses.models import Address

ORDER_STATUS_CHOICES = {
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('waiting_for_payment', 'Waiting for payment'),
    ('canceled', 'Canceled'),
}
ORDER_SHIPPING_STATUS_CHOICES = {
    ('shipped', 'Shipped'),
    ('not_shipped', 'Not yet shipped'),
}
PAYMENT_TYPE_CHOICES = {
    ('credit_card', 'Credit Card'),
    ('bank_deposit', 'Bank Deposit'),
}

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
    return "payment-confirmations/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

class PaymentConfirmation(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    email = models.EmailField()
    date_added = models.CharField(max_length=20, blank=True)
    bdo_branch = models.CharField(max_length=50, blank=True)
    full_name = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to=upload_image_path)
    total = models.DecimalField(default=0, max_digits=100, decimal_places=2)

    def __str__(self):
        return self.order_id

class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj, created

class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    shipping_address = models.ForeignKey('addresses.Address', related_name='shipping_address', on_delete=models.CASCADE, null=True, blank=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey('carts.Cart', on_delete=models.CASCADE)
    payment_type =  models.CharField(max_length=120, null=True, blank=True, choices=PAYMENT_TYPE_CHOICES)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_status = models.CharField(max_length=120, default='not_shipped', choices=ORDER_SHIPPING_STATUS_CHOICES)
    email_shipping_sent =  models.BooleanField(default=False)
    shipping_total = models.DecimalField(default=100, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True, auto_now=False)
    active = models.BooleanField(default=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        try:
            state = str(self.shipping_address.state)
            if state == "luzon":
                self.shipping_total = 110
            elif state == "visayas":
                self.shipping_total = 160
            elif state == "mindanao":
                self.shipping_total = 210

        except:
            pass
        new_total = math.fsum([cart_total + self.shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        print(self.total)
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.shipping_address
        total = self.total
        if billing_profile and shipping_address and billing_address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done(): # if returns true
            self.status = "paid"
            self.save()
        return self.status

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
    print("running")
    if created:
        print("updating")
        instance.update_total()

    if instance.shipping_status == 'shipped':
        if not instance.email_shipping_sent:
            print('sending email to', instance.billing_profile.email)

            subject = 'Your item is shipping!'
            message = ''
            email_from = 'Einghels Collection'
            recipient_list = [instance.billing_profile.email]
            msg_html = render_to_string('carts/email_shipping.html', {'some_params': 'asd'})
            html_message = loader.render_to_string(
                'carts/email_shipping.html',
                {
                    'order_id': instance.order_id,
                    'date_added': instance.date_added,
                    'order_status': instance.status,
                    'object': instance

                }
            )
            send_mail(subject, message, email_from, recipient_list, msg_html, html_message=html_message)

            instance.email_shipping_sent = True
            instance.save()
    # print("updating")
    # instance.update_total()
post_save.connect(post_save_order, sender=Order)