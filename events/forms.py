from django import forms
from users.models import User
from .models import Event
from location_field.forms.plain import PlainLocationField

class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'country', 'state', 'city', 'address', 'image', 'max_volunteers', 'category_on', 'price', 'registration_start_date', 'registration_end_date', 'organizer_name', 'organizer_email', 'skills_required']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(),
            'max_volunteers': forms.TextInput(attrs={'class': 'form-control'}),
            'category_on': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_start_date': forms.DateTimeInput(attrs={'type': 'date','class': 'form-control'}),
            'registration_end_date': forms.DateTimeInput(attrs={'type': 'date','class': 'form-control'}),
            'organizer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'organizer_email': forms.TextInput(attrs={'class': 'form-control'}),
            'skills_required': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class EventForm(forms.ModelForm):
    volunteers = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Event
        fields = '__all__'