import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from seller.models import Property
from home.models import Inquiry, Notification, CustomUser
from buyer.utils import convert_to_square_meters


def api_properties(request):
    """
    Asynchronous JSON endpoint returning real-time property listings and map markers.
    Supports filtering by location, price, size, type, and road.
    """
    properties = Property.objects.filter(status__iexact="available")

    query = request.GET.get('q', '').strip()
    if query:
        properties = properties.filter(
            title__icontains=query
        ) | properties.filter(
            municipality__icontains=query
        ) | properties.filter(
            district__icontains=query
        ) | properties.filter(
            province__icontains=query
        )

    district = request.GET.get('district', '').strip()
    if district:
        properties = properties.filter(district__icontains=district)

    municipality = request.GET.get('municipality', '').strip()
    if municipality:
        properties = properties.filter(municipality__icontains=municipality)

    prop_type = request.GET.get('type', '').strip()
    if prop_type:
        properties = properties.filter(property_type__iexact=prop_type)

    road = request.GET.get('road', '').strip()
    if road:
        properties = properties.filter(road_access__iexact=road)

    min_price = request.GET.get('min_price')
    if min_price:
        try:
            properties = properties.filter(price__gte=float(min_price))
        except ValueError:
            pass

    max_price = request.GET.get('max_price')
    if max_price:
        try:
            properties = properties.filter(price__lte=float(max_price))
        except ValueError:
            pass

    size = request.GET.get('size')
    unit = request.GET.get('unit', 'dhur')
    if size:
        try:
            properties = properties.filter(size__gte=float(size))
        except ValueError:
            pass

    results = []
    for p in properties:
        results.append({
            'id': p.id,
            'title': p.title,
            'price': float(p.price),
            'size': float(p.size),
            'size_unit': p.get_size_unit_display(),
            'lat': p.latitude,
            'lng': p.longitude,
            'type': p.property_type,
            'road': p.road_access,
            'location': p.location,
            'image': p.main_image,
            'detail_url': f"/seller/property/{p.id}/"
        })

    return JsonResponse({
        'status': 'success',
        'count': len(results),
        'properties': results
    })


@require_http_methods(["POST"])
def api_submit_inquiry(request):
    """
    Submits a buyer inquiry for a property and generates a notification for the seller.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Authentication required.'}, status=401)

    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST

    property_id = data.get('property_id')
    message = data.get('message', '').strip()

    if not property_id or not message:
        return JsonResponse({'status': 'error', 'message': 'Property ID and message are required.'}, status=400)

    try:
        property_obj = Property.objects.get(id=property_id)
    except Property.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Property not found.'}, status=404)

    inquiry = Inquiry.objects.create(
        user=request.user,
        property=property_obj,
        message=message
    )

    # Notify property owner in real-time
    Notification.objects.create(
        user=property_obj.owner,
        message=f"New inquiry from {request.user.full_name or request.user.email} on '{property_obj.title}'"
    )

    return JsonResponse({
        'status': 'success',
        'message': 'Inquiry submitted successfully.',
        'inquiry_id': inquiry.id
    })


def api_live_stats(request):
    """
    Returns platform-wide live metrics.
    """
    return JsonResponse({
        'total_properties': Property.objects.filter(status__iexact='available').count(),
        'total_inquiries': Inquiry.objects.count(),
        'total_users': CustomUser.objects.count(),
    })

