from django.contrib.auth.decorators import login_required  
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


# Home View (Redirect to dashboard if already logged in)
def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect to dashboard if the user is logged in
    return render(request, 'home/home.html')

# Login View (For AJAX)
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login successful.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid username or password.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

# Register View (For AJAX)
def register_view(request):
    if request.method == 'POST':
        # email = request.POST.get('email')
        # full_name = request.POST.get('fullName')
        # password = request.POST.get('password')
        # confirm_password = request.POST.get('confirmPassword')
        # if password != confirm_password:
        #     return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'})   
        # try:
        #     # Create user object
        #     user = User.objects.create_user(username=email, email=email, password=password)
        #     user.first_name = full_name
        #     user.save()
    #         # Automatically log in the user after registration
    #         login(request, user)

    #         return JsonResponse({'status': 'success', 'message': 'Registration successful! You are now logged in.'})
    #     except Exception as e:
    #         return JsonResponse({'status': 'error', 'message': 'Error creating account: ' + str(e)})

    # return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return 'success'
        else:
            form= UserCreationForm()
            return render(request, 'home/home.html', {'form': form})


# Logout View (For AJAX)
def logout_view(request):
    logout(request)
    return render(request, 'home/home.html')

# Protected View that requires login
@login_required
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')


# About View
def about_view(request):
    return render(request, 'about/about.html')

# Terms View
def terms_view(request):
    return render(request, 'terms/terms.html')

# Privacy View
def privacy_view(request):
    return render(request, 'privacy/privacy.html')       

# Contact View
def contact_view(request):
    return render(request, 'contact/contact.html', {'request': request})
