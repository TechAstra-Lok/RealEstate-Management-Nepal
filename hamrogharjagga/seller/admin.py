from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Property, PropertyMedia, Listing, Feature, Activity

class PropertyMediaInline(admin.TabularInline):
    model = PropertyMedia
    extra = 1 
    max_num = 10 
    fields = ('media_image', 'media_video')
    can_delete = True  

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'price', 'status', 'created_at', 'owner', 'views')
    search_fields = ('title', 'price', 'owner__email', 'municipality', 'district')
    list_filter = ('status', 'property_type', 'created_at', 'province', 'district')
    list_display_links = ('title', 'price')

    fieldsets = (
        (None, {
            'fields': (
                'title', 'property_type', 'road_access', 'province', 'district', 'municipality', 
                'ward', 'tole', 'size', 'size_unit', 'price', 'status', 'features', 'description', 
                'owner', 'best_time_to_contact', 'verified', 'latitude', 'longitude'
            )
        }),
    )

    inlines = [PropertyMediaInline]

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyMedia)
admin.site.register(Listing)
admin.site.register(Feature)
admin.site.register(Activity)
