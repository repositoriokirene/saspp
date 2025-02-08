from django.contrib import admin
from django.urls import include, path
from core import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/retail/', SignupView.as_view(), name='signup'),
    path('signup/corporate/', Signup2View.as_view(), name='signup2'),
    path('logout/', LogoutView, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
