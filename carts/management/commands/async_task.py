from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta

from carts.models import Cart
from order.models import Order

class Command(BaseCommand):
    try:
        help = 'Management task for cart and cancelling order.'

        def handle(self, *args, **kwargs):
            time_threshold = datetime.now() - timedelta(hours=1)
            cart_objects = Cart.objects.filter(timestamp__lt=time_threshold, is_done=False)

            for cart in cart_objects:
                for cart_item in cart.cartitem_set.all():
                    print(cart_item, cart_item.quantity, cart.id)
                    cart_item.item.inventory += cart_item.quantity  # return items
                    cart_item.item.save()
                    cart_item.save()
                cart.save()
                cart.delete()


            time = timezone.localtime(timezone.now()).strftime('%X')
            self.stdout.write("It's now %s" % time)
            #print(cart_objects)

            time_threshold = datetime.now() - timedelta(hours=72)
            order_objects = Order.objects.filter(timestamp__lt=time_threshold)

            for order in order_objects:
                for cart_item in order.cart.items():
                    print(cart_item, cart_item.quantity, cart.id)
                    cart_item.item.inventory += cart_item.quantity  # return items
                    cart_item.item.save()
                    cart_item.save()
                cart.save()
                cart.delete()

    except:
            pass