from django import forms
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class EditProfileForm(forms.ModelForm):

    email = forms.CharField()

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is taken")
        return email

class GuestForm(forms.Form):
    email = forms.EmailField()

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

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()

        return username

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

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password should be 8 characters or longer.")
        return password

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        for x in first_name:
            if x.isalpha() or x == ' ':
                continue
            else:
                raise forms.ValidationError("Letters only.")
                break
        first_name = re.sub(' +', ' ', first_name)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        for x in last_name:
            if x.isalpha() or x == ' ':
                continue
            else:
                raise forms.ValidationError("Letters only.")
                break
        last_name = re.sub(' +', ' ', last_name)
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        if len(username) < 5:
            raise forms.ValidationError("Username should have 5 characters or more.")

        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
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