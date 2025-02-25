from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Property

@login_required
def seller_dashboard_view(request):
    user = request.user  
    if user.role != "seller":
        return redirect("home:home")
    
    properties = Property.objects.filter(owner=user)
    inquiries = user.inquiries.all() 
    notifications = user.notifications.all()
    total_listings = properties.count()
    wishlist_items = user.wishlist.count()
    
    # Calculate total views efficiently using aggregation
    total_views = properties.aggregate(Sum('views'))['views__sum'] or 0  # Handles cases where there are no views yet
    
    # New inquiries are those with status 'new'
    new_inquiries = inquiries.filter(status='new').count()

    context = {
        'user': user,
        'properties': properties,
        'inquiries': inquiries,
        'total_listings': total_listings,
        'wishlist_items': wishlist_items,
        'total_views': total_views,
        'new_inquiries': new_inquiries,
        'notifications': notifications,
    }

    return render(request, 'seller/seller_dashboard.html', context)


@login_required
def sell(request):
    if request.user.role != "seller":
        return redirect("home:home")  # Restrict unauthorized access
    
    return render(request, "seller/sell_property.html")
