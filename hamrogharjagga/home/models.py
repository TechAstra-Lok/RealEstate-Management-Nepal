from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Your other custom fields here

    # Override the 'groups' field with a custom related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Change 'customuser_set' to something unique to avoid clashes
        blank=True
    )

    # Override the 'user_permissions' field with a custom related_name
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Change 'customuser_permissions_set' to something unique
        blank=True
    )

    pass
