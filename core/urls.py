from django.contrib import admin
from django.urls import include, path
from .views import HomePage, ReviewPage, AboutPage, ContactPage

urlpatterns = [
    path('', HomePage, name='index'),
    path('review/', ReviewPage, name='review_page'),
    path('about/', AboutPage, name='about_page'),
    path('contact/', ContactPage, name='contact_page'),
]
