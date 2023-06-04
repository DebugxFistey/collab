from django import forms
from .models import Contact
from django.conf import settings
from django.core.mail import send_mail

class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["price"].required = False

    firstname = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'shadow form-control', 'placeholder': 'First name'}),
    )

    lastname = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'shadow form-control', 'placeholder': 'Last Name'}),
    )

    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': 'shadow form-control', 'placeholder': 'Email'}),
    )
    message = forms.CharField(
        label='Write a message to send',
        help_text='Include all messages what you want to say',
        widget= forms.Textarea(attrs={"class": "shadow form-control"})
    )

    class Meta:
        model = Contact
        fields = (
            'firstname',
            'lastname',
            'email',
            'message',
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            subject = f'{instance.email} trying to contact you'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [instance.email, ]
            send_mail( subject, instance.message, email_from, recipient_list )
            instance.save()
        return instance