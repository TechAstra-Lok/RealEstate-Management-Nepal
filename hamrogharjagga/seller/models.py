import builtins
from django.db import models
from home.models import CustomUser, Inquiry


class Property(models.Model):
    PROPERTY_TYPE = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('agricultural', 'Agricultural'),
        ('industrial', 'Industrial'),
    ]
    ROAD_ACCESS = [
        ('pitched', 'Pitched Road'),
        ('gravel', 'Gravel Road'),
        ('soil', 'Soil Road'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
    ]
    CONTACT_TIME = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]
    SIZE_UNIT = [
        ('ropani', 'Ropani'),
        ('bigha', 'Bigha'),
        ('kattha', 'Kattha'),
        ('dhur', 'Dhur'),
    ]

    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='properties'
    )
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    title = models.CharField(max_length=200)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE)
    description = models.TextField()

    latitude = models.FloatField(default=27.7172)
    longitude = models.FloatField(default=85.3240)
    province = models.CharField(max_length=255, default='Bagmati')
    district = models.CharField(max_length=100, default='Kathmandu')
    municipality = models.CharField(max_length=255, default='Kathmandu')
    ward = models.CharField(max_length=10, default='1')
    tole = models.CharField(max_length=255, blank=True, null=True)

    road_access = models.CharField(
        max_length=100, choices=ROAD_ACCESS, default='pitched'
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    size = models.DecimalField(max_digits=8, decimal_places=2)
    size_unit = models.CharField(
        max_length=10, choices=SIZE_UNIT, default='dhur'
    )
    available_from = models.DateField(auto_now_add=True, null=True, blank=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='available'
    )
    verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    best_time_to_contact = models.CharField(
        max_length=100, choices=CONTACT_TIME, default='morning'
    )
    views = models.PositiveIntegerField(default=0)
    inquiries = models.ManyToManyField(
        Inquiry, related_name='properties', blank=True
    )
    features = models.ManyToManyField('Feature', blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def location(self):
        parts = [
            self.tole,
            f"Ward {self.ward}" if self.ward else None,
            self.municipality,
            self.district,
            self.province
        ]
        return ", ".join(
            [str(p).strip() for p in parts if p and str(p).strip()]
        )

    @property
    def main_image(self):
        first_media = self.media.filter(
            media_image__isnull=False
        ).exclude(media_image='').first()
        if first_media and first_media.media_image:
            try:
                return first_media.media_image.url
            except Exception:
                pass
        return '/static/assets/Card1.jpg'


class PropertyMedia(models.Model):
    property = models.ForeignKey(
        Property, related_name='media', on_delete=models.CASCADE
    )
    media_image = models.ImageField(
        upload_to='property_images/', blank=True, null=True
    )
    media_video = models.FileField(
        upload_to='property_videos/', blank=True, null=True
    )

    objects = models.Manager()

    @builtins.property
    def image(self):
        return self.media_image

    @builtins.property
    def video(self):
        return self.media_video

    def __str__(self):
        return f"Media for {self.property.title}"


class Feature(models.Model):
    name = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Listing(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contact_email = models.EmailField()
    listing_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    objects = models.Manager()

    class Meta:
        ordering = ['-listing_date']

    def __str__(self):
        return f"Listing: {self.property.title} by {self.seller.email}"


class Activity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        user_str = self.user.full_name or self.user.email
        formatted_time = self.timestamp.strftime('%Y-%m-%d %H:%M')
        return f"Activity by {user_str} on {formatted_time}"
