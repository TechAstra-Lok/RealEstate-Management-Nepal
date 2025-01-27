# views.py
from django.shortcuts import render

def home_view(request):
    return render(request, 'home/home.html')

def about_view(request):
    return render(request, 'about/about.html')

def terms_view(request):
    return render(request, 'terms/terms.html')  # Make sure the template exists

def privacy_view(request):
    return render(request, 'privacy/privacy.html')  # Make sure the template exists

def contact_view(request):
    return render(request, 'contact/contact.html', {'request': request})  # Make sure the template exists
