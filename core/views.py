from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from events.models import Event
from datetime import date

class Home(ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'events'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        context['events'] = Event.objects.filter(start_date__gt=today, is_cancelled=False).order_by("-created_at")
        return context
    
class ContactView(TemplateView):
    template_name = 'contact/contact-us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['requested_list'] = Event.objects.all().order_by("-created_at")
        return context