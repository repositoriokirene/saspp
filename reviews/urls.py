from django.contrib import admin
from django.urls import include, path
from .views import ServicesPage, ServicePage

urlpatterns = [
    path('service/', ServicePage, name='service_page'),
    path('service/<int:id>/', ServicePage, name='service_page_id'),
    path('services/', ServicesPage, name='services_page'),
]
