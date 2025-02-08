from django.urls import path
from core import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.IndexView, name='index'),
    path('sobre', views.SobreView, name='sobre')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
