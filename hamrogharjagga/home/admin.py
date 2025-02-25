from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'is_staff', 'is_active')  # Customize which fields you want in the list view
    search_fields = ('email', 'full_name')  # Allow searching by email and full name
    ordering = ('email', 'date_joined')  # Ordering by email and join date

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number', 'municipality', 'district')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
    )

    exclude = ('date_joined',)

    readonly_fields = ('date_joined',)  # Make 'date_joined' read-only

admin.site.register(CustomUser, CustomUserAdmin)
