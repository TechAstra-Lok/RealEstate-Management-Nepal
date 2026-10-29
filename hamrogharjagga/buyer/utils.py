UNIT_CONVERSIONS = {
    'ropani': 508.72,
    'bigha': 1360.92,
    'kattha': 338.04,
    'dhur': 16.81,
    'square_meter': 1.0,
}

def convert_to_square_meters(area_size, unit):
    conversion_factor = UNIT_CONVERSIONS.get(str(unit).lower(), 1.0)
    try:
        return float(area_size) * conversion_factor
    except (ValueError, TypeError):
        return 0.0

