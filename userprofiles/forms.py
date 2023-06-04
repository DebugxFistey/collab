from django import forms
from users.models import User
from taggit.forms import TagWidget
 

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'contact_no', 'bio', 'skills']
        
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic']