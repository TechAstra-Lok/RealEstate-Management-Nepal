from django.urls import path
from . import views

app_name = "buyer"

urlpatterns = [
    path("find_land/", views.find_land, name="find_land"),  
    path("wishlist/", views.wishlist, name="wishlist"), 
]
