# home/urls.py
from django.urls import path
from . import views  # Using 'views' as a module import

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('terms/', views.terms_view, name='terms'),  # Define the terms URL
    path('privacy/', views.privacy_view, name='privacy'),  # Define the privacy URL
    path('contact/', views.contact_view, name='contact'),  # Define the contact URL
]
