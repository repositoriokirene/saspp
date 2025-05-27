from django.shortcuts import render

# Create your views here.

def LoginPage(request):
    return render(request, 'loginPage.html')

def SignUpPage(request):
    return render(request, 'signupPage.html')