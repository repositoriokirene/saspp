from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

from accounts.models import Accounts, PasswordResetCode

User = get_user_model()

class CustomLoginForm(forms.Form):
    username = forms.CharField(label="Email ou Telefone")
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirme a senha')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email já está em uso.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise ValidationError("Este número de telefone já está em uso.")
        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password.isdigit():
            raise ValidationError("A senha não pode conter apenas números.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "As senhas não coincidem.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.username = self.cleaned_data["phone"]  # <=== username = phone
        if commit:
            user.save()
        return user
    
class PasswordResetRequestForm(forms.Form):
    identifier = forms.CharField(label='E-mail ou Telefone', max_length=100)

    def clean_identifier(self):
        data = self.cleaned_data['identifier']
        if '@' not in data and not data.isdigit():
            raise forms.ValidationError("Insira um email válido ou número de telefone.")
        return data
    
class CustomSetPasswordForm(SetPasswordForm):
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')

        if len(password1) < 8:
            raise forms.ValidationError("A senha deve conter pelo menos 8 caracteres.")

        if password1.isdigit():
            raise forms.ValidationError("A senha não pode conter apenas números.")

        if not re.search(r'[A-Za-z]', password1):
            raise forms.ValidationError("A senha deve conter pelo menos uma letra.")

        return password1
    
class PhoneResetRequestForm(forms.Form):
    phone = forms.CharField(label='Número de telefone')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not Accounts.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Nenhuma conta encontrada com este telefone.")
        return phone


class PhoneResetConfirmForm(forms.Form):
    phone = forms.CharField()
    code = forms.CharField(max_length=6)
    new_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        code = cleaned_data.get("code")

        try:
            obj = PasswordResetCode.objects.get(phone=phone, code=code)
            if obj.is_expired():
                raise forms.ValidationError("O código expirou.")
        except PasswordResetCode.DoesNotExist:
            raise forms.ValidationError("Código inválido.")

        return cleaned_data
