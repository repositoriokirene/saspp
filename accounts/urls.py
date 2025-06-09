from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .forms import CustomSetPasswordForm

urlpatterns = [
    path('login/', LoginPage, name='login_page'),
    path('signup/', SignUpPage, name='signup_page'),
    path('logut/', Logout, name='logout'),
    path('password_reset_request/', PasswordResetRequest, name='password_reset_request'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='PasswordResetConfirm.html', form_class=CustomSetPasswordForm
    ), name='password_reset_confirm'),
    path('password_reset_phone_confirm/', password_reset_phone_confirm, name='password_reset_phone_confirm'),
]
