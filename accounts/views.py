from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.http import Http404

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


from . import forms
from .models import GuestEmail
from billing.models import BillingProfile
from carts.models import Cart
from addresses.models import Address

from addresses.forms import AddressForm

def logout_page(request):
    if request.user.is_authenticated:
        cart_id = request.session.get("cart_id")
        print(cart_id, "is cart")
        if cart_id: # if exists
            cart = Cart.objects.get(id=cart_id)
            for cart_item in cart.cartitem_set.all():
                #print(cart_item, cart_item.quantity, cart_item.item, cart_item.item.inventory,)
                cart_item.item.inventory += cart_item.quantity # return items
                cart_item.item.save()
                cart_item.save()

            cart.save()
            cart.delete()
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
            new_user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name, is_active=False)
            #return redirect('accounts:login')

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)).decode(),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            context= {
                'title': "Just one more step..",
                'message': "We've sent you an email. Please confirm your email address to complete the registration and let's start shopping!"
            }

            return render(request, 'accounts/account_activation_messages.html', context)

        return render(request, "accounts/register.html", context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        context = {
            'title': "Your account is activated",
            'message': "Great! You can now login and start shopping!!"
        }

        return render(request, 'accounts/account_activation_messages.html', context)
    else:
        context = {
            'title': "Oops..",
            'message': "Your activation link seems to be invalid.."
        }

        return render(request, 'accounts/account_activation_messages.html', context)

def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                #messages.success(request, 'Your password was successfully updated!')
                return render(request, 'accounts/change_password_done.html')
            else:
                #messages.error(request, 'Please correct the error below.')
                pass
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'accounts/change_password.html', {
            'form': form
        })
    else:
        return redirect('accounts:login')

def account_info(request):
    return render(request, 'accounts/account_info.html')

def edit_address(request):
    address_id = request.GET.get("address_id")
    address_edit = request.GET.get("address_edit")
    address_delete = request.GET.get("address_delete")
    address_obj = Address.objects.get(id=address_id)
    if request.user.is_authenticated:
        if address_obj in request.user.billingprofile.address_set.all():
            if address_edit:
                form = AddressForm(instance=Address.objects.get(id=address_id))
                if request.method == 'POST':
                    form = AddressForm(request.POST or None)
                    if form.is_valid():
                        address_obj.address_line_1 = form.cleaned_data.get("address_line_1")
                        address_obj.address_line_2 = form.cleaned_data.get("address_line_2")
                        address_obj.city = form.cleaned_data.get("city")
                        address_obj.country = form.cleaned_data.get("country")
                        address_obj.state = form.cleaned_data.get("state")
                        address_obj.postal_code = form.cleaned_data.get("postal_code")
                        address_obj.save()
                        return render(request, 'accounts/account_info.html', {'address_id': address_id, 'address_delete': address_delete, 'form': form})
                    else:
                        return render(request, 'accounts/change_address.html', {'address_id': address_id, 'address_delete': address_delete, 'form': form})
            elif address_delete:
                address_obj.delete()
                return render(request, 'accounts/account_info.html', {'address_id': address_id, 'address_delete': address_delete})
        else:
            raise Http404
    else:
        raise Http404
    return render(request, 'accounts/change_address.html', {'address_id': address_id, 'address_delete': address_delete, 'form': form})

def change_email(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    user = request.user
    form = forms.EditProfileForm(request.POST or None, initial={'email':user.email})
    if request.method == 'POST':
        if form.is_valid():


            user.email = request.POST['email']
            billing_profile.email = request.POST['email']
            user.save()
            billing_profile.save()
            return redirect('accounts:account_info')

    context = {
        "form": form
    }

    return render(request, "accounts/change_email.html", context)