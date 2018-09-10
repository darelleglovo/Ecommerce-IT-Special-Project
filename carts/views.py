from django.views.generic.base import View
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# logout = clear cart and update inventory
from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm

from billing.models import BillingProfile
from accounts.models import GuestEmail
from orders.models import Order
from addresses.models import Address

from django.apps import apps

from .models import Cart, CartItem

Product = apps.get_model('products', 'Product')

class ItemCountView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get("cart_id")

            if cart_id is None:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                count = cart.items.count()
            return JsonResponse({"count": count})
        else:
            raise Http404
class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = "carts/view.html"

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)
        cart_id = self.request.session.get("cart_id")
        if cart_id == None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated:
            cart.user = self.request.user  # user sending request
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        out_of_stock = False
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete", False) # False default
        item_added = False
        if item_id: # if exists
            item_instance = get_object_or_404(Product, id=item_id)
            qty = int(request.GET.get("qty", 1))
            try:
                if qty < 1:
                    delete_item = True
            except:
                raise Http404
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
            item_instance.inventory
            if created:
                if  item_instance.inventory <= 0:
                    qty = 0
                    out_of_stock = True
                else:
                    print("created > ",  item_instance.inventory)
                    item_added = True
                    item_instance.inventory -= qty
                    cart_item.quantity = qty
                    cart_item.save()
            elif delete_item:
                item_instance.inventory += cart_item.quantity
                cart_item.delete()
                print("deleted > ", item_instance.inventory)
            else:
                if  item_instance.inventory <= 0:
                    qty = 0
                    out_of_stock = True
                else:
                    print( item_instance.inventory, qty, cart_item.quantity)
                    item_instance.inventory -= (qty - cart_item.quantity)
                    cart_item.quantity = qty
                    cart_item.save()
            item_instance.full_clean()
            item_instance.save()
            #print(item_instance.inventory)

        if request.is_ajax():
            return JsonResponse({"deleted": delete_item, "item_added": item_added, "out_of_stock": out_of_stock})

        context = {
            "object": self.get_object()
        }
        template = self.template_name
        return render(request, template, context)



def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.items.count() == 0:
        return redirect("carts:cart")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            del request.session['cart_id']
            return redirect("/cart/success")

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
    }
    return render(request, "carts/checkout.html", context)







