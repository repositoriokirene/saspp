import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.decorators import is_auth
from accounts.models import Accounts, PasswordResetCode
from .forms import CustomLoginForm, CustomUserCreationForm, PasswordResetRequestForm, PhoneResetConfirmForm
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
import requests

# Create your views here.

User = get_user_model()

@is_auth()
def LoginPage(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login efetuado com sucesso.')
                return redirect('index')
            else:
                messages.error(request, 'Credenciais inválidas.')
    return render(request, 'loginPage.html')

@is_auth()
def SignUpPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso. Faça login.")
            return redirect('login_page')
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = CustomUserCreationForm()

    context = {
        'form':form
    }
    return render(request, 'signupPage.html', context)

def Logout(request):
    logout(request)
    messages.success(request, "Sessão encerrada com sucesso.")
    return redirect('login_page')
    
def send_reset_code(phone):
    code = str(random.randint(100000, 999999))

    PasswordResetCode.objects.filter(phone=phone).delete()
    PasswordResetCode.objects.create(phone=phone, code=code)

    payload = {
        "message": {
            "api_key_app": "prdf3f7c1fc9c4664fd51762cb058",
            "phone_number": phone,
            "message_body": f"Seu código de recuperação de senha no SASPP é: {code}"
        }
    }
    try:
        response = requests.post("https://www.telcosms.co.ao/api/v2/send_message", json=payload)
        return response.status_code == 200
    except Exception:
        return False

def PasswordResetRequest(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            try:
                user = User.objects.get(email=identifier) if '@' in identifier else User.objects.get(phone=identifier)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

                if '@' in identifier:
                    # Via email
                    user.email_user("Recuperação de senha - SASPP", f"Use este link para redefinir sua senha do SASPP: {reset_url}\n\nCaso ")
                    messages.success(request, "Um link foi enviado para seu e-mail.")
                else:
                    # Via SMS
                    if send_reset_code(user.phone):
                        messages.success(request, "Um código foi enviado por SMS.")
                        return redirect('password_reset_phone_confirm')
                    else:
                        messages.error(request, "Falha ao enviar SMS. Tente novamente.")
                        return redirect('password_reset_request')

                return redirect('login_page')

            except User.DoesNotExist:
                messages.error(request, "Usuário não encontrado.")
    else:
        form = PasswordResetRequestForm()

    return render(request, 'PasswordResetRequest.html', {'form': form})

def password_reset_phone_confirm(request):
    if request.method == 'POST':
        form = PhoneResetConfirmForm(request.POST)
        if form.is_valid():
            print("Form válido!")
            user = User.objects.get(phone=form.cleaned_data['phone'])
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            PasswordResetCode.objects.filter(phone=form.cleaned_data['phone']).delete()
            messages.success(request, 'Senha redefinida com sucesso. Faça login.')
            return redirect('login_page')

    else:
        form = PhoneResetConfirmForm()
    return render(request, 'PasswordResetPhoneConfirm.html', {'form': form})