# properties/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('find_land/', views.find_land_view, name='find_land'),  # This will render properties.html
]
