from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from .forms import CreateEventForm
from .models import Event, VolunteerAssignment, VolunteerRequest
from users.models import User
from core.utils import is_ajax
from django.http import JsonResponse
from django.views.generic import View, ListView, CreateView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.minix import VolunteerRequestPermissionMixin, ProviderRequestPermissionMixin
from django.urls import reverse
from django.contrib import messages
from datetime import date


class EventCreateView(LoginRequiredMixin, ProviderRequestPermissionMixin, CreateView):
    model = Event
    form_class = CreateEventForm
    template_name = 'provider/event/create_event.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('event-detail', args=(self.object.pk,))
    
class EventListView(LoginRequiredMixin, ProviderRequestPermissionMixin, TemplateView):
    template_name = 'provider/event/event_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['requested_list'] = Event.objects.filter().order_by("-created_at")
        return context

class EventDetailView(LoginRequiredMixin, ProviderRequestPermissionMixin, DetailView):
    model = Event
    template_name = 'provider/event/event_detail.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event= Event.objects.get(id=self.kwargs['pk'])
        context['assigned_volunteer'] = VolunteerAssignment.objects.filter(event=event)
        return context
    
class VolunteerRequestListView(LoginRequiredMixin, ProviderRequestPermissionMixin, TemplateView):
    template_name = 'provider/event/requested_event.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['requested_list'] = VolunteerRequest.objects.filter(accepted=False, rejected=False)
        return context
    
    
class VolunteerAssignedListView(LoginRequiredMixin, ProviderRequestPermissionMixin, TemplateView):
    template_name = 'provider/event/assigned_event.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['requested_list'] = VolunteerAssignment.objects.all()
        return context
    
class VolunteerRejectedListView(LoginRequiredMixin, ProviderRequestPermissionMixin, TemplateView):
    template_name = 'provider/event/rejected_event.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['requested_list'] = VolunteerRequest.objects.filter(accepted=False, rejected=True)
        
        return context

class AssignVolunteerView(LoginRequiredMixin, ProviderRequestPermissionMixin, View):
    def post(self, request, *args, **kwargs):
        current_url = request.path
        request_id = request.POST.get('request_id')
        volunteer_request = VolunteerRequest.objects.get(id=request_id)
        volunteer_request.accepted = True
        volunteer_request.save()
        assign = VolunteerAssignment.objects.create(event=volunteer_request.event, user=volunteer_request.user)
        messages.add_message(request, messages.INFO, "Successfully Assigned.")
        return redirect('request_list')
    
class RejectedVolunteerView(LoginRequiredMixin, ProviderRequestPermissionMixin, View):
    def post(self, request, *args, **kwargs):
        request_id = request.POST.get('request_id')
        volunteer_request = VolunteerRequest.objects.get(id=request_id)
        volunteer_request.accepted = False
        volunteer_request.rejected = True
        volunteer_request.save()
        messages.add_message(request, messages.INFO, "Rejected Successfully.")
        return redirect('request_list')
    
class RemoveAssignVolunteerView(LoginRequiredMixin, ProviderRequestPermissionMixin, View):
    def post(self, request, *args, **kwargs):
        request_id = request.POST.get('request_id')
        volunteer_request = VolunteerAssignment.objects.get(id=request_id)
        volunteer_request.delete()
        messages.add_message(request, messages.INFO, "Remove Successfully.")
        return redirect('assign_list')
    
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    try:
        requested_user = VolunteerRequest.objects.get(user=request.user, event=event)
    except:
        requested_user = None
        assign_event_user = None
    return render(request, 'event/event_detail.html', {'event': event, 'requested_user':requested_user})


class VolunteerRequestView(LoginRequiredMixin, VolunteerRequestPermissionMixin, View):
    def post(self, request):
        if is_ajax(request):
            event_id = request.POST.get('event_id')
            try:
                event = get_object_or_404(Event, id=event_id)
                if VolunteerRequest.objects.filter(user=request.user, event=event).count() > 0:
                    return JsonResponse({"status": True, "msg":"Already Requested"}, status=200)
                else:
                    VolunteerRequest.objects.create(user=request.user, event=event)
                    return JsonResponse({"status": True, "msg":"Requested Successfully"}, status=200)
            except:
                return JsonResponse({"status": False, "msg":"Something went wrong1"}, status=200)
        return JsonResponse({"status": False, "msg":"Something went wrong2"}, status=200)


class SearchView(ListView):
    model = Event
    template_name = 'event/search_result.html'
    context_object_name = 'results'

    def get_queryset(self):
        query1 = self.request.GET.get('city', '')
        query2 = self.request.GET.get('state', '')
        query3 = self.request.GET.get('country', '')

        queryset = super().get_queryset()
        today = date.today()
        
        results = Event.objects.none()

        if query1.strip():
            results |= Event.objects.filter(city__icontains=query1, start_date__gt=today, is_cancelled=False).order_by("-created_at")

        if query2.strip():
            results |= Event.objects.filter(state__icontains=query2, start_date__gt=today, is_cancelled=False).order_by("-created_at")

        if query3.strip():
            results |= Event.objects.filter(country__icontains=query3, start_date__gt=today, is_cancelled=False).order_by("-created_at")

        if results == Event.objects.none():
            results = Event.objects.filter(start_date__gt=today, is_cancelled=False).order_by("-created_at")
        return results
    
    
class EventListsView(ListView):
    model = Event
    template_name = 'event/search_result.html'
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        context['results'] = Event.objects.filter(start_date__gt=today, is_cancelled=False).order_by("-created_at")
        return context