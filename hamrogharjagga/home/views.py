from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from .models import CustomUser    
from home.forms import RegisterForm, LoginForm



def home_view(request):
    if request.user.is_authenticated:
        if request.user.role == "seller":
            return redirect("seller:dashboard")
        elif request.user.role == "buyer":
            return redirect("buyer:find_land")
        return render(request, "home/home.html")
    else:
        return render(request, "home/home.html") 


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            
            if password1 != password2:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Passwords do not match. Please try again.'
                })
            
            try:
                user = form.save(commit=False)
                user.username = user.email  # Assuming email as username
                user.set_password(password2)  # Hash the password
                user.save()

                return JsonResponse({
                    'status': 'success',
                    'message': 'Registration successful! Please log in.',
                    'redirect_url': reverse('home:login')
                })
            except Exception as e:
                messages.error(request, "An error occurred. Please try again.")
                return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred: ' + str(e)})
        else:
            print(form.errors)
            return JsonResponse({
                'status': 'error',
                'message': 'Registration failed. Please check the form for errors.'
            })
    else:
        form = RegisterForm()
        return render(request, "home/home.html", {"form": form})
    

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            
            # Authenticate the user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)

                # Redirect based on user role
                if user.role == 'buyer':
                    return redirect('buyer:find_land')  # Redirect buyer to 'find_property'
                elif user.role == 'seller':
                    return redirect('seller:dashboard')  # Redirect seller to 'dashboard'
                else:
                    return redirect('home:home')  # Default redirect if role is neither buyer nor seller
            else:
                form.add_error('email', 'Invalid email or password')
        else:
            print(form.errors)  # Debugging: Check form errors if any
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
