from django import template
from products.models import Product

register = template.Library()

@register.simple_tag
def get_critical_level():
    critical = Product.objects.filter(inventory__lte=10).count()
    return critical