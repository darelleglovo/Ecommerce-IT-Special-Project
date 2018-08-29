from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

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
            if created:
                item_added = True
            if delete_item:
                cart_item.delete()
            else:
                cart_item.quantity = qty
                cart_item.save()

        if request.is_ajax():
            return JsonResponse({"deleted": delete_item, "item_added": item_added})

        context = {
            "object": self.get_object()
        }
        template = self.template_name
        return render(request, template, context)

class CheckoutView(DetailView):
    model = Cart
    template_name = "carts/checkout_view.html"

    def get_object(self, *args, **kwargs):
        cart_id = self.request.session.get("cart_id")
        if cart_id == None:
            return redirect("carts:cart")
        cart = Cart.objects.get(id=cart_id)
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        if not self.request.user.is_authenticated:
            context["user_auth"] = False
        return context








