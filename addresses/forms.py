from django import forms

from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            #'billing_profile',
            #'address_type',
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            'state',
            'postal_code'
        ]
        labels = {
            'address_line_1': ('Address line 1 (house #, street, brgy)'),
            'address_line_2': ('Address line 2 (optional)'),
        }

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['country'].required = False
            self.fields['country'].widget.attrs['readonly'] = True

    def clean_country(self):
        return "Philippines"