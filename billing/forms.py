from django import forms
from django.contrib.auth import get_user_model
PAYMENT_TYPE_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('bank_deposit', 'BDO Bank Deposit'),
]
class PaymentTypeForm(forms.Form):
    payment_type = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES, widget=forms.RadioSelect())

