from django.urls import path
from . import views

app_name = "seller"

urlpatterns = [
    path("dashboard/", views.seller_dashboard_view, name="dashboard"),  
    path("sell/", views.sell, name="sell"),  
]
