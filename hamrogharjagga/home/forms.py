from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    municipality = forms.CharField(max_length=255, required=False)
    district = forms.CharField(max_length=255, required=False)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)
    payment_method = forms.ChoiceField(
        choices=[('esewa', 'eSewa'), ('khalti', 'Khalti'), ('paypal', 'PayPal')],
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ["email", "full_name", "phone_number", "municipality", "district", "role", "payment_method"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            email = email.lower().strip()
            if CustomUser.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"].lower().strip()
        user.email = email
        user.username = email
        user.full_name = self.cleaned_data["full_name"]
        user.phone_number = self.cleaned_data.get("phone_number", "")
        user.municipality = self.cleaned_data.get("municipality", "")
        user.district = self.cleaned_data.get("district", "")
        user.role = self.cleaned_data.get("role", "buyer")
        user.user_type = user.role
        user.payment_method = self.cleaned_data.get("payment_method", "esewa")
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label="Password", required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Password", required=False)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password") or cleaned_data.get("password2")

        if not email:
            raise forms.ValidationError("Email is required.")
        if not password:
            raise forms.ValidationError("Password is required.")

        email = email.lower().strip()
        user = authenticate(username=email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise forms.ValidationError("This account has been deactivated.")

        cleaned_data["user"] = user
        cleaned_data["email"] = email
        cleaned_data["password"] = password
        return cleaned_data
