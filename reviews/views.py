from django.shortcuts import render

# Create your views here.

def ServicePage(request):
    return render(request, 'servicePage.html')


def ServicesPage(request):
    return render(request, 'servicesPage.html')