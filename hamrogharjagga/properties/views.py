from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def properties_view(request):
    return render(request, 'properties.html')
