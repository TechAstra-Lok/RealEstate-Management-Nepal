from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.db import models

# Custom manager for handling user creation
class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)  # Encrypt password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        """
        Create and return a superuser with the necessary privileges.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, password, **extra_fields)


# Custom user model inheriting from AbstractUser
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    municipality = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Set email as the unique identifier (username) instead of username
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['full_name']  # 'email' is already the unique identifier

    # Use the custom manager for creating users and superusers
    objects = CustomUserManager()

    # Ensure the username is set to the email if not provided
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        if not self.user_type and self.role:
            self.user_type = self.role
        elif not self.role and self.user_type:
            self.role = self.user_type
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    

class Inquiry(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='inquiries')
    message = models.TextField()
    property = models.ForeignKey('seller.Property', on_delete=models.CASCADE, related_name='property_inquiries')
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('new', 'New'), ('replied', 'Replied')], default='new')

    def __str__(self):
        return f"Inquiry by {self.user.username} for property {self.property.id}"
        
class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email} - {self.message[:20]}"
