from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from . import forms
# git test 2
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/login")

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/products')
    else:
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
                return redirect("/products")
            else:
                # Return an 'invalid login' error message.
                print("Error")
                messages.error(request, 'username or password not correct')

                return redirect('login')

        return render(request, "auth/login.html", context)

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
            return redirect('login')
        return render(request, "auth/register.html", context)

def registered(request):
    return render(request, "registered.html")

def home_page(request):
    #print(request.session.get("first_name", "Unknown"))
    context = {
        "title": "hello World!"
    }
    #return render(request, "home_page.html", {})
    return redirect('products:home')

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
