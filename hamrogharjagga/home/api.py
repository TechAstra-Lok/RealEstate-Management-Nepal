import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from seller.models import Property, Activity
from home.models import Inquiry, Notification, CustomUser
from buyer.utils import convert_to_square_meters


def api_properties(request):
    """
    Asynchronous JSON endpoint returning real-time property listings and map.
    Supports filtering by location, price, area size, type, road, and sorting.
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

    province = request.GET.get('province', '').strip()
    if province:
        properties = properties.filter(province__icontains=province)

    district = request.GET.get('district', '').strip()
    if district:
        properties = properties.filter(district__icontains=district)

    municipality = request.GET.get('municipality', '').strip()
    if municipality:
        properties = properties.filter(municipality__icontains=municipality)

    prop_type = (
        request.GET.get('type') or
        request.GET.get('property_type', '').strip()
    )
    if prop_type:
        properties = properties.filter(property_type__iexact=prop_type)

    road = (
        request.GET.get('road') or
        request.GET.get('road_access', '').strip()
    )
    if road:
        properties = properties.filter(road_access__iexact=road)

    min_price = request.GET.get('min_price')
    if min_price:
        try:
            properties = properties.filter(price__gte=float(min_price))
        except (ValueError, TypeError):
            pass

    max_price = request.GET.get('max_price')
    if max_price:
        try:
            properties = properties.filter(price__lte=float(max_price))
        except (ValueError, TypeError):
            pass

    size = request.GET.get('size') or request.GET.get('area_size')
    unit = request.GET.get('unit') or request.GET.get('area_unit', 'dhur')
    if size:
        try:
            target_sqm = convert_to_square_meters(float(size), unit)
            matched_ids = []
            for p in properties:
                p_sqm = convert_to_square_meters(float(p.size), p.size_unit)
                if p_sqm >= target_sqm:
                    matched_ids.append(p.id)
            properties = properties.filter(id__in=matched_ids)
        except (ValueError, TypeError):
            pass

    sort_option = request.GET.get('sort', 'price-asc')
    sort_options = {
        "price-asc": "price",
        "price-desc": "-price",
        "area-asc": "size",
        "area-desc": "-size",
        "date-desc": "-created_at",
    }
    properties = properties.order_by(sort_options.get(sort_option, "price"))

    results = []
    for p in properties:
        results.append({
            'id': p.id,
            'title': p.title,
            'price': float(p.price) if p.price is not None else 0.0,
            'size': float(p.size) if p.size is not None else 0.0,
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


@csrf_exempt
@require_http_methods(["POST"])
def api_submit_inquiry(request):
    """
    Submits a buyer inquiry for a property and generates notifications.
    """
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Authentication required. Please login first.'
        }, status=401)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    property_id = data.get('property_id')
    message = str(data.get('message', '')).strip()

    if not property_id or not message:
        return JsonResponse({
            'status': 'error',
            'message': 'Property ID and inquiry message are required.'
        }, status=400)

    try:
        property_obj = Property.objects.get(id=property_id)
    except Property.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Property not found.'
        }, status=404)

    inquiry = Inquiry.objects.create(
        user=request.user,
        property=property_obj,
        message=message
    )

    property_obj.inquiries.add(inquiry)

    sender_name = request.user.full_name or request.user.email
    Notification.objects.create(
        user=property_obj.owner,
        message=f"New inquiry from {sender_name} on '{property_obj.title}'"
    )

    Activity.objects.create(
        user=request.user,
        message=f"Sent inquiry on property '{property_obj.title}'"
    )

    return JsonResponse({
        'status': 'success',
        'message': 'Your inquiry has been sent to the property owner.',
        'inquiry_id': inquiry.id
    })


def api_live_stats(request):
    """
    Returns platform-wide live metrics.
    """
    return JsonResponse({
        'total_properties': Property.objects.filter(
            status__iexact='available'
        ).count(),
        'total_inquiries': Inquiry.objects.count(),
        'total_users': CustomUser.objects.count(),
    })
