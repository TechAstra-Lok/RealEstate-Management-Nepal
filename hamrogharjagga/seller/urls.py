from django.urls import path
from . import views

app_name = "seller"

urlpatterns = [
    path("dashboard/", views.seller_dashboard_view, name="dashboard"),  
    path("sell/", views.sell, name="sell"),  
    path("settings/", views.settings, name="settings"), 
    path("update_profile/", views.update_profile, name="update_profile"),
    path("My_Property/", views.My_Property, name="My_Property"),
    path("property/<int:property_id>/", views.property_detail, name="property_detail"),
]
