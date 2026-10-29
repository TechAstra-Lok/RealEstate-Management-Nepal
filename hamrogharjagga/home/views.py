from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from home.forms import RegisterForm, LoginForm
from seller.models import Property


def home_view(request):
    if request.user.is_authenticated:
        user_role = getattr(request.user, 'role', '')
        if user_role == "seller":
            return redirect("seller:dashboard")
        elif user_role == "buyer":
            return redirect("buyer:find_land")

    featured_properties = Property.objects.filter(
        status__iexact="available"
    ).order_by('-views')[:6]
    return render(
        request,
        "home/home.html",
        {'featured_properties': featured_properties}
    )


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        is_ajax = (
            request.headers.get('x-requested-with') == 'XMLHttpRequest'
            or request.POST.get('is_ajax') == 'true'
            or 'full_name' in request.POST
        )

        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                if user.role == 'seller':
                    redirect_url = reverse('seller:dashboard')
                else:
                    redirect_url = reverse('buyer:find_land')

                if is_ajax:
                    return JsonResponse({
                        'status': 'success',
                        'message': (
                            'Registration successful! '
                            'Welcome to HamroGhajagga.'
                        ),
                        'redirect_url': redirect_url
                    })
                return redirect(redirect_url)
            except Exception as e:
                if is_ajax:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Registration error: {str(e)}'
                    })
                messages.error(request, f"Error: {e}")
        else:
            if is_ajax:
                first_error = ""
                for field, error_list in form.errors.items():
                    first_error = f"{field}: {error_list[0]}"
                    break
                err_msg = (
                    first_error or
                    'Validation failed. Please check form errors.'
                )
                return JsonResponse({
                    'status': 'error',
                    'message': err_msg
                })
            messages.error(
                request,
                "Registration failed. Please check form errors."
            )
    else:
        form = RegisterForm()

    return render(request, "home/home.html", {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        is_ajax = (
            request.headers.get('x-requested-with') == 'XMLHttpRequest'
            or request.POST.get('is_ajax') == 'true'
            or 'password2' in request.POST
            or 'password' in request.POST
        )

        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            if getattr(user, 'role', '') == 'seller':
                redirect_url = reverse('seller:dashboard')
            else:
                redirect_url = reverse('buyer:find_land')

            if is_ajax:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Login successful!',
                    'redirect_url': redirect_url
                })
            return redirect(redirect_url)
        else:
            if is_ajax:
                err_list = form.non_field_errors()
                msg = (
                    err_list[0] if err_list else
                    "Invalid email or password. Please try again."
                )
                return JsonResponse({'status': 'error', 'message': msg})
            messages.error(request, "Invalid email or password.")
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
