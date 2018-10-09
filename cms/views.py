from django.shortcuts import render
from .models import AboutUs, ContactUs

# Create your views here.
def about(request):
    about_us = AboutUs.objects.all().first()
    context = {
        "about_us": about_us
    }
    return render(request, "cms/about_us.html", context)

def contact(request):
    contact_us = ContactUs.objects.all().first()
    context = {
        "contact_us": contact_us
    }
    return render(request, "cms/contact_us.html", context)