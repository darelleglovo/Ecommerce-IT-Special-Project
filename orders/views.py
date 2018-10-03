from django.shortcuts import render, redirect
from . import forms
from .models import PaymentConfirmation, Order

# Create your views here.
def upload_payment_proof(request):
    form = forms.UploadForm(request.POST, request.FILES or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = PaymentConfirmation()
        print(form.cleaned_data)
        obj.order_id = form.cleaned_data.get("order_id")
        obj.email = form.cleaned_data.get("email")
        obj.date_added = form.cleaned_data.get("date_added")
        obj.bdo_branch = form.cleaned_data.get("bdo_branch")
        obj.full_name = form.cleaned_data.get("full_name")
        obj.image = form.cleaned_data.get("image")
        obj.total = form.cleaned_data.get("total")
        obj.save()
        return redirect('orders:success')
    return render(request, "orders/upload-payment-proof.html", context)

def upload_done(request):
    return render(request, "orders/success.html")

def past_orders(request):
    orders = Order.objects.filter(billing_profile__email=request.user.email)
    context = {
        "orders": orders
    }
    return render(request, "orders/past-orders.html", context)


    # order_id = models.CharField(max_length=120, blank=True)
    # email = models.CharField(max_length=20, blank=True)
    # date_added = models.DateTimeField()
    # bdo_branch = models.CharField(max_length=50, blank=True)
    # full_name = models.CharField(max_length=120, blank=True)
    # image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    # total = models.DecimalField(default=0, max_digits=100, decimal_places=2)