from django import forms
from .models import PaymentConfirmation

class UploadForm(forms.ModelForm):
    class Meta:
        model = PaymentConfirmation
        fields = [
            #'billing_profile',
            #'address_type',
            'order_id',
            'email',
            'date_added',
            'bdo_branch',
            'full_name',
            'image',
            'total'
        ]
        #
        # order_id = models.CharField(max_length=120, blank=True)
        # email = models.CharField(max_length=20, blank=True)
        # date_added = models.DateTimeField()
        # bdo_branch = models.CharField(max_length=50, blank=True)
        # full_name = models.CharField(max_length=120, blank=True)
        # image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
        # total = models.DecimalField(default=0, max_digits=100, decimal_places=2)

# class UploadForm(forms.Form):
#     order_id = forms.CharField(widget=forms.TextInput(
#         attrs={
#             "_icon": "user",
#             "_align": "left"
#         }
#     ))
#     email = forms.EmailField(widget=forms.EmailInput(
#         attrs={
#             "_icon": "envelope",
#             "_align": "left"
#         }
#     ))
#     payment_date = forms.DateTimeField(widget=forms.TextInput(
#         attrs={
#             'class': 'datepicker'
#         }
#     ))
#     BDO_branch = forms.CharField(widget=forms.TextInput(
#         attrs={
#             "_icon": "user",
#             "_align": "left"
#         }
#     ))
#     full_name = forms.CharField(widget=forms.TextInput(
#         attrs={
#             "_icon": "user",
#             "_align": "left"
#         }
#     ))
#     upload_payment_proof = forms.ImageField()
#     amount = forms.DecimalField()