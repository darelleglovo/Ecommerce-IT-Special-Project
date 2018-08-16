from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={
            "class":"form-control",
            "placeholder":"Your full name"
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class": "form-control",
            "placeholder": "Your email"
        }
    ))
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            "class":"form-control",
            "placeholder":"Your message"
        }
    ))
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gmail.")
        return email

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "_icon": "user",
            "_align": "left"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "_icon": "lock",
            "_align": "left"
        }
    ))

class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "_icon": "user",
            "_align": "left"
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "_icon": "user",
            "_align": "left"
        }
    ))
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "_icon": "user",
            "_align": "left"
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "_icon": "envelope",
            "_align": "left"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "_icon": "lock",
            "_align": "left"
        }
    ))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "_icon": "lock",
            "_align": "left"
        }
    ))
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is taken")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            print("error")
            raise forms.ValidationError("Passwords must match.")
        return data