from django.shortcuts import render

# Create your views here.

def HomePage(request):
    return render(request, 'homePage.html')

def ReviewPage(request):
    return render(request, 'reviewPage.html')

def AboutPage(request):
    return render(request, 'aboutPage.html')

def ContactPage(request):
    return render(request, 'contactPage.html')