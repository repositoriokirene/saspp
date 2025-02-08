from django.shortcuts import render

# Create your views here.

def IndexView(request):
    return render(request, 'index.html')

def SobreView(request):
    return render(request, 'sobre.html')