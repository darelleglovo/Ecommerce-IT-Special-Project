from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from . import forms
from .models import GuestEmail

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/login")

def guest_register_view(request):
    if request.user.is_authenticated:
        return redirect('/products')
    else:
        form = forms.GuestForm(request.POST or None)
        context = {
            "form": form
        }
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if form.is_valid():
            email = form.cleaned_data.get("email")
            new_guest_email = GuestEmail.objects.create(email=email)
            request.session['guest_email_id'] = new_guest_email.id
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/register/")

        return redirect("/register/")


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/products')
    else:
        form = forms.LoginForm(request.POST or None)
        context = {
            "form": form
        }
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            print(user)
            print(request.user.is_authenticated)
            if user is not None:
                login(request, user)
                try:
                    del request.session['guest_email_id']
                except:
                    pass
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                else:
                    return redirect("/products")
            else:
                # Return an 'invalid login' error message.
                print("Error")
                messages.error(request, 'username or password not correct')

                return redirect('accounts:login')

        return render(request, "accounts/login.html", context)

User = get_user_model()
def register_page(request):
    if request.user.is_authenticated:
        return redirect('/products')
    else:
        form = forms.RegisterForm(request.POST or None)
        context = {
            "form": form
        }
        if form.is_valid():
            print(form.cleaned_data)
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            new_user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            return redirect('accounts:login')
        return render(request, "accounts/register.html", context)