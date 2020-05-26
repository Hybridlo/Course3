from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class SignupForm(forms.Form):
    email = forms.EmailField(max_length=200, label="Університетська пошта (@knu.ua):")
    email2 = forms.EmailField(max_length=200, required=False, label="Додаткова пошта (не обов'язково):")
    password1 = forms.CharField(max_length=40, label="Пароль:", widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=40, label="Підтвердіть пароль:", widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=30, label="Ім'я:")
    last_name = forms.CharField(max_length=150, label="Прізвище:")

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@knu.ua" not in data:
            raise forms.ValidationError("Використовуйте лише пошту університету")
        return data

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        validate_password(password2)

        if not password2:
            raise forms.ValidationError("Підтвердіть ваш пароль")
        if password1 != password2:
            raise forms.ValidationError("Паролі не збігаються")
        return password2

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200, label="Пошта:")
    password = forms.CharField(max_length=40, label="Пароль:", widget=forms.PasswordInput())

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@knu.ua" not in data:
            raise forms.ValidationError("Використовуйте лише пошту університету")
        return data

class UserSettings(forms.Form):
    first_name = forms.CharField(max_length=30, required=False, label="Ім'я:")
    last_name = forms.CharField(max_length=150, required=False, label="Прізвище:")
    email2 = forms.EmailField(max_length=200, required=False, label="Додаткова пошта:")
    curr_password = forms.CharField(max_length=40, label="Пароль (обов'язково):", widget=forms.PasswordInput())
    password1 = forms.CharField(max_length=40, required=False, label="Новий пароль:", widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=40, required=False, label="Підтвердіть пароль:", widget=forms.PasswordInput())
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password2 == "":
            return password2

        validate_password(password2)

        if not password2:
            raise forms.ValidationError("Підтвердіть ваш пароль")
        if password1 != password2:
            raise forms.ValidationError("Паролі не збігаються")
        return password2

class UserAddInfo(forms.Form):
    info = forms.CharField(widget=forms.Textarea(), label="Додаткова інформація:")