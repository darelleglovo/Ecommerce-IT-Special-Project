from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from . import forms

def registered(request):
    return render(request, "registered.html")

def home_page(request):
    context = {
        "title": "hello World!"
    }
    return render(request, "home_page.html", context)

def about_page(request):
    return render(request, "home_page.html", {})

def contact_page(request):
    contact_form = forms.ContactForm(request.POST or None)
    context = {
        "title": "Contact page",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    # if request.method == "POST":
    #     print(request.POST)
    #     print(request.POST.get('fullname'))
    return render(request, "contact/view.html", context)
