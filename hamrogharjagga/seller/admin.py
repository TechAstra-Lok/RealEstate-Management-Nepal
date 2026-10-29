from django.contrib import admin
from .models import Property, PropertyMedia, Listing, Feature, Activity

class PropertyMediaInline(admin.TabularInline):
    model = PropertyMedia
    extra = 1 
    max_num = 10 
    fields = ('media_image', 'media_video')
    can_delete = True  

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'price', 'status', 'verified', 'created_at', 'owner', 'views')
    search_fields = ('title', 'price', 'owner__email', 'municipality', 'district', 'phone_number', 'email')
    list_filter = ('status', 'verified', 'property_type', 'created_at', 'province', 'district')
    list_display_links = ('title', 'price')
    list_editable = ('status', 'verified')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'property_type', 'description', 'status', 'verified')
        }),
        ('Location Details', {
            'fields': ('province', 'district', 'municipality', 'ward', 'tole', 'latitude', 'longitude')
        }),
        ('Specifications & Pricing', {
            'fields': ('size', 'size_unit', 'price', 'road_access', 'features')
        }),
        ('Contact Information', {
            'fields': ('owner', 'phone_number', 'email', 'best_time_to_contact')
        }),
    )

    inlines = [PropertyMediaInline]

class PropertyMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'media_image', 'media_video')
    list_filter = ('property',)

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'seller', 'price', 'is_active', 'listing_date')
    list_filter = ('is_active', 'listing_date')
    search_fields = ('property__title', 'seller__email', 'contact_email')

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__email', 'message')

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyMedia, PropertyMediaAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Activity, ActivityAdmin)
