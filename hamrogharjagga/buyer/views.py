from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Property, Location
from django.http import JsonResponse

def find_land(request):
    # Retrieve filter parameters
    location = request.GET.get('location', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    area_size = request.GET.get('area_size')
    sort_option = request.GET.get('sort', 'price-asc')

    # Fetch approved and available properties
    properties = Property.objects.filter(status="Available", verified=True)

    # Apply filters
    if location:
        properties = properties.filter(location__name__icontains=location)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    if area_size:
        unit = request.GET.get('area_unit', 'square_meter')  # Default to square meter
        area_size_in_meters = convert_to_square_meters(float(area_size), unit)
        properties = properties.filter(size__gte=area_size_in_meters)

    # Sorting logic
    sort_options = {
        "price-asc": "price",
        "price-desc": "-price",
        "area-asc": "size",
        "area-desc": "-size",
    }
    properties = properties.order_by(sort_options.get(sort_option, "price"))

    # Check if request is AJAX (for JSON response)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        properties_data = [
            {
                'title': property.title,
                'price': property.price,
                'latitude': property.latitude,
                'longitude': property.longitude,
                'description': property.description,
                'size': property.size,
                'location': property.location.name,  # Assuming 'name' is the location name
            }
            for property in properties
        ]
        return JsonResponse(properties_data, safe=False)

    # **Render HTML template if it's a normal request**
    return render(request, 'buyer/properties.html', {'properties': properties})


def convert_to_square_meters(area, unit):
    conversion_factors = {
        'ropani': 508.72,  # 1 Ropani = 508.72 square meters
        'aana': 508.72 / 16,
        'bigha': 1361.8,  # 1 Bigha = 1361.8 square meters
        'kattha': 338.0,   # 1 Kattha = 338 square meters
    }
    return area * conversion_factors.get(unit, 1)  # Default is square meters





@login_required
def wishlist(request):    
    return render(request, "buyer/wishlist.html")