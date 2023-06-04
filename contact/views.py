from django.shortcuts import render, HttpResponse,redirect,get_object_or_404,reverse

from .models import Contact
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.views import View
from django.http import HttpResponsePermanentRedirect
from .forms import ContactForm
from django.http import HttpResponseRedirect

class ContactFormView(View):
    form_class = ContactForm
    initial = {'key': 'value'}
    template_name = 'contact/contact-us.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Message Sent Successfully. We will contact you soon...")
            return HttpResponseRedirect('/contact/form/')

        return render(request, self.template_name, {'form': form})