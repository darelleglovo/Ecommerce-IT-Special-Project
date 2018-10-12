from django.db import models
from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', '-'),
    ('shipping', 'Shipping')
)
STATES = (
    ('luzon', 'Luzon'),
    ('visayas', 'Visayas'),
    ('mindanao', 'Mindanao')
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default='Philippines')
    state = models.CharField(max_length=120, choices=STATES)
    postal_code = models.CharField(max_length=120)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return "{line1}\n{line2}\n{city} City\n{state}, {postal}\n{country}".format(
            line1 = self.address_line_1,
            line2 = self.address_line_2 or "", #if none then ""
            city = self.city,
            state = self.state.capitalize(),
            postal = self.postal_code,
            country = self.country
        )