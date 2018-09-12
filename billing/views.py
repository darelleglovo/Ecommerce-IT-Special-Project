from django.shortcuts import render

import stripe
stripe.api_key = "sk_test_pFGDr0qx9NJOMp1jhrWueACt"
STRIPE_PUB_KEY = 'pk_test_rILfT84BLIkg02QiRTcXHz5H' # to frontend

def payment_method_view(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY})