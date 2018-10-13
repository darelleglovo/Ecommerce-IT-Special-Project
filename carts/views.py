from django.conf import settings
from django.views.generic.base import View
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.template import loader


# logout = clear cart and update inventory
from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm
from billing.forms import PaymentTypeForm

from billing.models import BillingProfile
from accounts.models import GuestEmail
from orders.models import Order
from addresses.models import Address

from django.apps import apps

from .models import Cart, CartItem

Product = apps.get_model('products', 'Product')

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_pFGDr0qx9NJOMp1jhrWueACt")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", 'pk_test_rILfT84BLIkg02QiRTcXHz5H') # to frontend
stripe.api_key = STRIPE_SECRET_KEY

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
        try:
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
        except:
            del self.request.session['cart_id']
            self.request.session['is_bank_transfer'] = False

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        out_of_stock = False
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete", False) # False default
        item_added = False
        if item_id: # if exists
            item_instance = get_object_or_404(Product, id=item_id)
            try:
                qty = int(request.GET.get("qty", 1))
            except:
                raise Http404

            try:
                if qty < 1:
                    delete_item = True
            except:
                raise Http404

            try: # changes
                cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
            except:
                return redirect("carts:cart")

            if created:
                if  item_instance.inventory <= 0:
                    qty = 0
                    out_of_stock = True
                    cart_item.qty = 0
                    cart_item.delete()

                    print('out of stock')
                    if request.is_ajax():
                        print('out of stock')
                        return JsonResponse(
                            {"deleted": delete_item, "item_added": None, "out_of_stock": out_of_stock})
                else:
                    print("created > ",  item_instance.inventory)
                    item_added = True
                    if item_instance.inventory >= qty:
                        item_instance.inventory -= qty
                        cart_item.quantity = qty
                        cart_item.save()
                    else:
                        qty = 0
                        out_of_stock = True
                        print("qty greater than inventory")
                        cart_item.qty =  0
                        cart_item.delete()
                        return JsonResponse(
                            {"deleted": delete_item, "item_added": None, "out_of_stock": out_of_stock})

                        print("zzzzzzzzzzzzzzzzzzzzzzz")
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

def cancel_order(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        order_obj.shipping_address = None
        order_obj.payment_type = None
        order_obj.save()

    return redirect("carts:cart")

def cancel_mode_of_payment(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        order_obj.payment_type = None
        order_obj.save()

    return redirect("carts:checkout")

def cancel_address(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        order_obj.shipping_address = None
        order_obj.save()

    return redirect("carts:checkout")


def checkout_home(request):
    payment_type_form = PaymentTypeForm(request.POST or None)
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
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.update_total()
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == "POST":
        is_prepared = order_obj.check_done()
        if not order_obj.payment_type:
            if payment_type_form.is_valid():
                print(payment_type_form.cleaned_data)
                order_obj.payment_type =  payment_type_form.cleaned_data.get("payment_type")
                order_obj.save()
                return redirect("carts:checkout")
        else:
            print(order_obj.payment_type)
            if order_obj.payment_type == "credit_card":
                print("CC True")
                if is_prepared:
                    did_charge, crg_msg = billing_profile.charge(order_obj)
                    if did_charge:
                        order_obj.mark_paid()
                        order_obj.cart.is_done = True # changes
                        order_obj.cart.save()# changes
                        order_obj.save()# changes
                        del request.session['cart_id']
                        if not billing_profile.user:
                            billing_profile.set_cards_inactive()
                        request.session['is_bank_transfer'] = False

                        subject = 'Thank you for shopping with us!'
                        message = ''
                        email_from = 'Einghels Collection'
                        recipient_list = [request.user.email]
                        msg_html = render_to_string('carts/email_card.html', {'some_params': 'asd'})
                        html_message = loader.render_to_string(
                            'carts/email_card.html',
                            {
                                'order_id': order_obj.order_id,
                                'date_added': order_obj.date_added,
                                'order_status': order_obj.status,
                                'object': order_obj

                            }
                        )
                        send_mail(subject, message, email_from, recipient_list, msg_html, html_message=html_message)

                        return redirect("carts:success")
                    else:
                        print(crg_msg)
                        return redirect("carts:checkout")
            elif order_obj.payment_type == "bank_deposit":
                order_obj.status = 'waiting_for_payment'
                order_obj.cart.is_done = True # changes
                order_obj.cart.save()# changes
                order_obj.save()
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                request.session['is_bank_transfer'] = True

                subject = 'Thank you for shopping with us!'
                message = ''
                email_from = 'Einghels Collection'
                recipient_list = [request.user.email]
                msg_html = render_to_string('carts/email.html', {'some_params': 'asd'})
                html_message = loader.render_to_string(
                    'carts/email.html',
                    {
                        'order_id': order_obj.order_id,
                        'date_added': order_obj.date_added,
                        'order_status': order_obj.status,
                        'object': order_obj


                    }
                )
                send_mail(subject, message, email_from, recipient_list, msg_html, html_message=html_message)

                return redirect("carts:success")

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
        "payment_type_form": payment_type_form,
    }
    return render(request, "carts/checkout.html", context)



def chechout_done_view(request):
    return render(request, "carts/checkout-done.html")



