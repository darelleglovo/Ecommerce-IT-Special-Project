from django.contrib import admin

from .models import Order, PaymentConfirmation

class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'shipping_status', 'payment_type']
    list_filter = ['status', 'shipping_status', 'payment_type']
    class Meta:
        model = Order

admin.site.register(Order, OrderAdmin)
admin.site.register(PaymentConfirmation)
