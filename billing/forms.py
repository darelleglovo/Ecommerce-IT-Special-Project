from django import forms
from django.contrib.auth import get_user_model
PAYMENT_TYPE_CHOICES = {
    ('credit_card', 'Credit Card'),
    ('bank_deposit', 'Bank Deposit'),
}
class PaymentTypeForm(forms.Form):
    payment_type = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES, widget=forms.RadioSelect())
class UploadForm(forms.Form):
    order_id = forms.CharField(widget=forms.TextInput(
        attrs={
            "_icon": "user",
            "_align": "left"
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "_icon": "envelope",
            "_align": "left"
        }
    ))
    payment_date = forms.DateTimeField(widget=forms.TextInput(
        attrs={
            'class': 'datepicker'
        }
    ))
    BDO_branch = forms.CharField(widget=forms.TextInput(
        attrs={
            "_icon": "user",
            "_align": "left"
        }
    ))
    full_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "_icon": "user",
            "_align": "left"
        }
    ))
    upload_payment_proof = forms.ImageField()
    amount = forms.DecimalField()
