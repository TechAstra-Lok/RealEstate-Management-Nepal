from django import forms
from .models import Property, PropertyMedia, Feature
from home.models import CustomUser

class PropertyForm(forms.ModelForm):
    media_images = forms.FileField(required=False)
    media_videos = forms.FileField(required=False)

    class Meta:
        model = Property
        fields = [
            'title', 'property_type', 'phone_number', 'email', 'road_access',
            'province', 'district', 'municipality', 'ward', 'tole',
            'size', 'size_unit', 'price', 'best_time_to_contact', 'description',
            'latitude', 'longitude'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter property title', 'class': 'form-control', 'id': 'id_title'}),
            'property_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_property_type'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter phone number', 'class': 'form-control', 'id': 'id_phone_number'}),  
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email', 'class': 'form-control', 'id': 'id_email'}),  
            'road_access': forms.Select(attrs={'class': 'form-control', 'id': 'id_road_access'}),
            'province': forms.TextInput(attrs={'placeholder': 'Enter province', 'class': 'form-control', 'id': 'id_province'}),
            'district': forms.TextInput(attrs={'placeholder': 'Enter district', 'class': 'form-control', 'id': 'id_district'}),
            'municipality': forms.TextInput(attrs={'placeholder': 'Enter municipality', 'class': 'form-control', 'id': 'id_municipality'}),
            'ward': forms.TextInput(attrs={'placeholder': 'Enter ward number', 'class': 'form-control', 'id': 'id_ward'}),
            'tole': forms.TextInput(attrs={'placeholder': 'Enter tole name', 'class': 'form-control', 'id': 'id_tole'}),
            'size': forms.NumberInput(attrs={'placeholder': 'Enter size', 'class': 'form-control', 'id': 'id_size'}),
            'size_unit': forms.Select(attrs={'class': 'form-control', 'id': 'id_size_unit'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter price', 'class': 'form-control', 'id': 'id_price'}),
            'best_time_to_contact': forms.Select(attrs={'class': 'form-control', 'id': 'id_best_time_to_contact'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description', 'class': 'form-control', 'id': 'id_description', 'rows': 4}),
            'latitude': forms.HiddenInput(attrs={'id': 'latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'longitude'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PropertyForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.owner = self.user
        if not instance.latitude:
            instance.latitude = 27.7172
        if not instance.longitude:
            instance.longitude = 85.3240
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class PropertyMediaForm(forms.ModelForm):
    class Meta:
        model = PropertyMedia
        fields = ['media_image', 'media_video']
        widgets = {
            'media_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_media_image'}),
            'media_video': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_media_video'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone_number', 'municipality', 'district', 'profile_picture']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'municipality': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This email is already taken.")
        return email

