from django.db import models
from home.models import CustomUser
from seller.models import Property



class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishlist')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    STATUS_CHOICES = [
        ('read', 'Read'),
        ('unread', 'Unread')
    ]

    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
    created_at = models.DateTimeField(auto_now_add=True)

class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
