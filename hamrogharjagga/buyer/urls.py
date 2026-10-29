from django.urls import path
from . import views

app_name = "buyer"

urlpatterns = [
    path("find_land/", views.find_land, name="find_land"),  
    path("wishlist/", views.wishlist, name="wishlist"), 
    path("wishlist/add/<int:property_id>/", views.add_to_wishlist, name="add_wishlist"),
    path("wishlist/remove/<int:wishlist_id>/", views.remove_from_wishlist, name="remove_wishlist"),
]
