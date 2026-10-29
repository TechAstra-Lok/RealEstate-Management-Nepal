from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
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
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered!")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
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
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Password", required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password2")

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password")
            cleaned_data["user"] = user

        return cleaned_data
