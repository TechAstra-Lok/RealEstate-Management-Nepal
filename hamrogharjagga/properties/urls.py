from django.urls import path
from .views import properties_view

urlpatterns = [
    path('', properties_view, name='properties'),
]
