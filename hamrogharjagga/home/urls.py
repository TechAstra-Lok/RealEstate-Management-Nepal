# home/urls.py
from django.urls import path
from home import views

app_name = "home"  # This defines the namespace for this app

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.user_login, name="login"),  
    path('logout/', views.user_logout, name="logout"),
    path('register/', views.user_register, name="register"),
    path('about/', views.about_view, name="about"),
    path('terms/', views.terms_view, name="terms"),
    path('privacy/', views.privacy_view, name="privacy"),
    path('contact/', views.contact_view, name="contact"),
]
