from django.db import models
from home.models import CustomUser
from home.models import Inquiry 

class Property(models.Model):
    PROPERTY_TYPE = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial')
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('rented', 'Rented')
    ]

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE)
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    size = models.DecimalField(max_digits=8, decimal_places=2)
    latitude = models.FloatField()
    longitude = models.FloatField()
    available_from = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    inquiries = models.ManyToManyField(Inquiry, related_name='properties', blank=True)

    def __str__(self):
        return self.title

class PropertyMedia(models.Model):
    property = models.ForeignKey(Property, related_name='media', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    video = models.FileField(upload_to='property_videos/', blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media for {self.property.title} - {self.media_type}"
    
class Listing(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contact_email = models.EmailField()
    listing_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ['-listing_date']
