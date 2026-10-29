import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Property, Activity, PropertyMedia
from home.models import CustomUser, Inquiry
from buyer.models import Wishlist
from .forms import PropertyForm, ProfileUpdateForm, PropertyMediaForm


@login_required
def seller_dashboard_view(request):
    user = request.user 
    if user.role != "seller":
        return redirect("home:home")
    
    properties = Property.objects.filter(owner=user).order_by('-created_at')
    inquiries = Inquiry.objects.filter(property__owner=user).order_by('-date_created')
    notifications = user.notifications.all().order_by('-created_at')[:10]
    total_listings = properties.count()
    wishlist_items = Wishlist.objects.filter(property__owner=user).count()
    
    total_views = properties.aggregate(Sum('views'))['views__sum'] or 0 
    active_properties = properties.filter(status__iexact='available').count() 
    recent_activities = Activity.objects.filter(user=user).order_by('-timestamp')[:5]
    new_inquiries = inquiries.filter(status='new').count()

    chart_labels = [p.created_at.strftime('%Y-%m-%d') for p in properties[:10]]
    chart_views = [p.views for p in properties[:10]]

    context = {
        'user': user,
        'user_profile': user,
        'properties': properties,
        'inquiries': inquiries,
        'total_listings': total_listings,
        'wishlist_items': wishlist_items,
        'total_views': total_views,
        'new_inquiries': new_inquiries,
        'notifications': notifications,
        'recent_activities': recent_activities,
        'chart_labels': json.dumps(chart_labels),
        'chart_views': json.dumps(chart_views),
    }

    return render(request, 'seller/dashboard.html', context)


@login_required
def sell(request):
    if request.user.role != "seller":
        messages.error(request, "Only registered sellers can list properties.")
        return redirect("home:home")

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, user=request.user)
        media_form = PropertyMediaForm(request.POST, request.FILES)
        
        if form.is_valid():
            property_instance = form.save()

            # Handle media uploads
            media_image = request.FILES.get('media_image') or request.FILES.get('media_images')
            media_video = request.FILES.get('media_video') or request.FILES.get('media_videos')

            if media_image:
                PropertyMedia.objects.create(property=property_instance, media_image=media_image)

            if media_video:
                PropertyMedia.objects.create(property=property_instance, media_video=media_video)

            Activity.objects.create(user=request.user, message=f"Listed property '{property_instance.title}'")
            messages.success(request, "Property submitted successfully!")
            return redirect('seller:My_Property')
        else:
            messages.error(request, "There was an error submitting your property. Please check the fields.")
    else:
        form = PropertyForm()
        media_form = PropertyMediaForm()

    return render(request, 'seller/sell.html', {'form': form, 'media_form': media_form})


@login_required
def My_Property(request):
    properties = Property.objects.filter(owner=request.user).order_by('-created_at')
    paginator = Paginator(properties, 9)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'seller/property_list.html', {'properties': page_obj})


def property_detail(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    # Increment view count
    Property.objects.filter(id=property_id).update(views=F('views') + 1)
    property_obj.refresh_from_db()
    
    return render(request, 'seller/property_detail.html', {'property': property_obj})


@login_required
def settings(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('seller:dashboard') 
        else:
            messages.error(request, "There was an error updating your profile.")
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'seller/settings.html', {'form': form, 'user': user})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Your profile has been updated!')
            return redirect('seller:dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'seller/update_profile.html', {'form': form})
