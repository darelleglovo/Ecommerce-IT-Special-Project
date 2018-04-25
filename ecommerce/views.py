from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from . import forms

def login_page(request):
    form = forms.LoginForm(request.POST or None)
    context = {
        "form": form
    }
    print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        print(user)
        print(request.user.is_authenticated)
        if user is not None:
            print(request.user.is_authenticated)
            login(request, user)
            # Redirect to a success page.
            #context['form'] = forms.LoginForm()
            return redirect("/login")
        else:
            # Return an 'invalid login' error message.
            print("Error")

    return render(request, "auth/login.html", context)

def register_page(request):
    form = forms.LoginForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
    return render(request, "auth/login.html")

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
