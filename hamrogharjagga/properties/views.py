# properties/views.py
from django.shortcuts import render
from .models import Property

def find_land_view(request):
    properties = Property.objects.all()
    
    return render(request, 'properties/properties.html', {'properties': properties})
