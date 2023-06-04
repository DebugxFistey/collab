from allauth.account.forms import SignupForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Column,
    Layout,
    Row,
)
 
ACCOUNT_TYPE =(
    ('', '---------'),
    ("Volunteer", "Volunteer"),
    ("Provider", "Provider"),
)
 
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    email = forms.EmailField(max_length=255, label='Email')
    account_type = forms.ChoiceField(choices = ACCOUNT_TYPE)
    contact_no = forms.IntegerField()
    skills = forms.TextInput()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['account_type'].widget.attrs['class'] = 'form-control'
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-lg-6', style="padding-bottom:20px;"),
                Column('last_name', css_class='form-group col-lg-6', style="padding-bottom:20px;"),
                Column('email', css_class='form-group col-lg-6', style="padding-bottom:20px;"),
                Column('account_type', css_class='form-group col-lg-6', style="padding-bottom:20px;"),
                Column('contact_no', css_class='form-group col-lg-6', style="padding-bottom:20px;"),
                Column('skills', css_class='form-group col-lg-6', style="padding-bottom:20px;"),
                Column('password1', css_class='form-group col-lg-6', style="padding-bottom:20px;"),
                Column('password2', css_class='form-group col-lg-6', style="padding-bottom:20px;"),
                css_class='row',
            ))
        return helper
    
 
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if self.cleaned_data['account_type'] == 'Volunteer':
            user.is_volunteer = True
        if self.cleaned_data['account_type'] == 'Provider':
            user.is_provider = True
        user.contact_no = self.cleaned_data['contact_no']
        user.save()
        return user