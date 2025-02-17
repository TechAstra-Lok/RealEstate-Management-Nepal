from django.db import models
from home.models import CustomUser  # Importing CustomUser model

# Property Type Choices
class Property(models.Model):
    RESIDENTIAL = 'Residential'
    COMMERCIAL = 'Commercial'
    PROPERTY_TYPES = [
        (RESIDENTIAL, 'Residential'),
        (COMMERCIAL, 'Commercial'),
    ]
    
    # Property Status Choices
    STATUS_AVAILABLE = 'Available'
    STATUS_SOLD = 'Sold'
    STATUS_RENTED = 'Rented'
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_SOLD, 'Sold'),
        (STATUS_RENTED, 'Rented'),
    ]

    # Fields for the Property model
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(
        max_length=20, choices=PROPERTY_TYPES, default=RESIDENTIAL
    )
    location_address = models.CharField(max_length=255)
    location_district = models.CharField(max_length=255)
    location_province = models.CharField(max_length=255)
    description = models.TextField()
    property_size = models.DecimalField(max_digits=8, decimal_places=2)
    available_from = models.DateField()
    images = models.ImageField(upload_to='property_images/', blank=True, null=True)
    videos = models.FileField(upload_to='property_videos/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
