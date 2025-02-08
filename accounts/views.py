# views.py
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from accounts.forms import CustomAuthenticationForm, SignupForm, SignupForm2
#from .forms import SignupForm

User = get_user_model()

class LoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm

# Para particulares
class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'signup.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_company = False 
        self.object.save()

        login(self.request, self.object)
        return redirect(self.get_success_url())

#Para empresas
class Signup2View(CreateView):
    model = User
    form_class = SignupForm2
    template_name = 'signup2.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_company = True 
        self.object.save()

        login(self.request, self.object)
        return redirect(self.get_success_url())
    

def LogoutView(request):
    logout(request)
    return redirect('/auth/login/')
