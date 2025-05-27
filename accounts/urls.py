from django.contrib import admin
from django.urls import include, path
from .views import LoginPage, SignUpPage

urlpatterns = [
    path('login/', LoginPage, name='login_page'),
    path('signup/', SignUpPage, name='signup_page'),
]
