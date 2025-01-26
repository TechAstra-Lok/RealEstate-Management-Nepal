from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import DashboardItem

def dashboard_view(request):
    items = DashboardItem.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'dashboard/dashboard.html', context)
