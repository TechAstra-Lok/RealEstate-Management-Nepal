from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from .models import CustomUser, Inquiry, Notification
from home.forms import RegisterForm, LoginForm
from seller.models import Property


def home_view(request):
    if request.user.is_authenticated:
        if request.user.role == "seller":
            return redirect("seller:dashboard")
        elif request.user.role == "buyer":
            return redirect("buyer:find_land")
    
    featured_properties = Property.objects.filter(status__iexact="available").order_by('-views')[:6]
    return render(request, "home/home.html", {'featured_properties': featured_properties})


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('role') is not None
        
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)  # Automatically login upon successful registration
                redirect_url = reverse('seller:dashboard') if user.role == 'seller' else reverse('buyer:find_land')
                
                if is_ajax:
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Registration successful! Welcome to HamroGhajagga.',
                        'redirect_url': redirect_url
                    })
                return redirect(redirect_url)
            except Exception as e:
                if is_ajax:
                    return JsonResponse({'status': 'error', 'message': f'Registration error: {str(e)}'})
                messages.error(request, f"Error: {e}")
        else:
            errors = form.errors.as_text()
            if is_ajax:
                return JsonResponse({'status': 'error', 'message': f'Validation failed: {errors}'})
            messages.error(request, "Registration failed. Please check form errors.")
    else:
        form = RegisterForm()
    
    return render(request, "home/home.html", {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'password2' in request.POST
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                redirect_url = reverse('seller:dashboard') if user.role == 'seller' else reverse('buyer:find_land')
                
                if is_ajax:
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Login successful!',
                        'redirect_url': redirect_url
                    })
                return redirect(redirect_url)
            else:
                if is_ajax:
                    return JsonResponse({'status': 'error', 'message': 'Invalid email or password. Please try again.'})
                form.add_error(None, 'Invalid email or password.')
        else:
            if is_ajax:
                return JsonResponse({'status': 'error', 'message': 'Please provide a valid email and password.'})
    else:
        form = LoginForm()

    return render(request, 'home/home.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home:home') 


def about_view(request):
    return render(request, "about/about.html")


def terms_view(request):
    return render(request, "terms/terms.html")


def privacy_view(request):
    return render(request, "privacy/privacy.html")


def contact_view(request):
    return render(request, "contact/contact.html")
