import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from seller.models import Property
from .models import Wishlist
from .utils import convert_to_square_meters 


def property_list(request):
    """
    Public listings view / redirect to find_land.
    """
    return redirect("buyer:find_land")


@login_required
def find_land(request):
    user = request.user 
    if getattr(user, 'role', '') == "seller":
        return redirect("seller:dashboard")

    # Retrieve filter parameters
    municipality = request.GET.get('municipality', '').strip()
    district = request.GET.get('district', '').strip()
    province = request.GET.get('province', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    area_size = request.GET.get('area_size', '').strip()
    area_unit = request.GET.get('area_unit', 'dhur')
    property_type = request.GET.get('property_type', '').strip()
    road_access = request.GET.get('road_access', '').strip()
    sort_option = request.GET.get('sort', 'price-asc')

    properties = Property.objects.filter(status__iexact="available")

    # Apply location filters
    if municipality:
        properties = properties.filter(municipality__icontains=municipality)
    if district:
        properties = properties.filter(district__icontains=district)
    if province:
        properties = properties.filter(province__icontains=province)
    if property_type:
        properties = properties.filter(property_type__iexact=property_type)
    if road_access:
        properties = properties.filter(road_access__iexact=road_access)

    # Apply price range filters
    if min_price:
        try:
            properties = properties.filter(price__gte=float(min_price))
        except (ValueError, TypeError):
            pass
    if max_price:
        try:
            properties = properties.filter(price__lte=float(max_price))
        except (ValueError, TypeError):
            pass

    # Apply accurate land area size filter converted to square meters
    if area_size:
        try:
            target_sqm = convert_to_square_meters(float(area_size), area_unit)
            matched_ids = []
            for p in properties:
                p_sqm = convert_to_square_meters(float(p.size), p.size_unit)
                if p_sqm >= target_sqm:
                    matched_ids.append(p.id)
            properties = properties.filter(id__in=matched_ids)
        except (ValueError, TypeError):
            pass

    sort_options = {
        "price-asc": "price",
        "price-desc": "-price",
        "area-asc": "size",
        "area-desc": "-size",
        "date-desc": "-created_at",
    }
    properties = properties.order_by(sort_options.get(sort_option, "price"))

    # Prepare JSON data for Leaflet Map
    markers_data = []
    for p in properties:
        markers_data.append({
            'id': p.id,
            'title': p.title,
            'price': float(p.price) if p.price is not None else 0.0,
            'size': float(p.size) if p.size is not None else 0.0,
            'size_unit': p.get_size_unit_display(),
            'lat': p.latitude,
            'lng': p.longitude,
            'location': p.location,
            'image': p.main_image,
            'detail_url': f"/seller/property/{p.id}/"
        })

    context = {
        'properties': properties,
        'markers_json': json.dumps(markers_data),
        'municipality': municipality,
        'district': district,
        'province': province,
        'min_price': min_price,
        'max_price': max_price,
        'area_size': area_size,
        'area_unit': area_unit,
        'property_type': property_type,
        'road_access': road_access,
        'sort_option': sort_option,
    }
    return render(request, 'buyer/properties.html', context)


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('property').order_by('-created_at')
    return render(request, "buyer/wishlist.html", {'wishlist_items': wishlist_items})


@login_required
def add_to_wishlist(request, property_id):
    user = request.user
    property_obj = get_object_or_404(Property, id=property_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=user, property=property_obj)
    return JsonResponse({
        "status": "success",
        "created": created,
        "message": "Property added to your wishlist!" if created else "Property is already in your wishlist."
    })


@login_required
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    wishlist_item.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Removed from wishlist.'})
    return redirect("buyer:wishlist")
