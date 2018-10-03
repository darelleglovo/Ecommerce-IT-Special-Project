from django.contrib import admin

from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Order, PaymentConfirmation

def make_shipped(modeladmin, request, queryset):
    queryset.update(shipping_status='shipped')
    for object in queryset:
        object.save()


def make_not_shipped(modeladmin, request, queryset):
    queryset.update(shipping_status='not_shipped')


make_shipped.short_description = "Mark selected product as shipped"
make_not_shipped.short_description = "Mark selected product as not yet shipped"

class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'shipping_status', 'payment_type']
    list_filter = ['status', 'shipping_status', 'payment_type']

    actions = [make_shipped, make_not_shipped]
    class Meta:
        model = Order

admin.site.register(Order, OrderAdmin)
admin.site.register(PaymentConfirmation)
