from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User
from events.models import VolunteerRequest, VolunteerAssignment
from .forms import UserProfileForm, ProfilePictureForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from core.minix import VolunteerRequestPermissionMixin, ProviderRequestPermissionMixin


class ProviderProfileView(LoginRequiredMixin, ProviderRequestPermissionMixin, DetailView):
    model = User
    template_name = 'provider/profile/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['requested_list'] = VolunteerRequest.objects.filter(accepted=False, rejected=False)
        context['rejected_event'] = VolunteerRequest.objects.filter(user=self.request.user, rejected=True)
        context['accepted_event'] = VolunteerRequest.objects.filter(user=self.request.user, accepted=True)
        context['assign_event'] = VolunteerAssignment.objects.filter(user=self.request.user)
        return context

# Create your views here.
class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'
    success_url = reverse_lazy('profile')
        
    def get_context_data(self,*args, **kwargs):
        context = super(UserProfileView, self).get_context_data(*args,**kwargs)
        context['profile_form'] = UserProfileForm(instance=self.request.user)
        context['rejected_event'] = VolunteerRequest.objects.filter(user=self.request.user, rejected=True)
        context['accepted_event'] = VolunteerRequest.objects.filter(user=self.request.user, accepted=True)
        context['assign_event'] = VolunteerAssignment.objects.filter(user=self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
class ProfilePictureUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfilePictureForm
    template_name = 'profile/profile_pic.html'
    success_url = reverse_lazy('profile_pic_update')

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self,*args, **kwargs):
        context = super(ProfilePictureUpdateView, self).get_context_data(*args,**kwargs)
        context['rejected_event'] = VolunteerRequest.objects.filter(user=self.request.user, rejected=True)
        context['accepted_event'] = VolunteerRequest.objects.filter(user=self.request.user, accepted=True)
        context['assign_event'] = VolunteerAssignment.objects.filter(user=self.request.user)
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()  # Save the updated profile picture
        return response
    

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'profile/change_password.html'
    success_url = reverse_lazy('change_password')
    
    def get_context_data(self,*args, **kwargs):
        context = super(PasswordChangeView, self).get_context_data(*args,**kwargs)
        context['rejected_event'] = VolunteerRequest.objects.filter(user=self.request.user, rejected=True)
        context['accepted_event'] = VolunteerRequest.objects.filter(user=self.request.user, accepted=True)
        context['assign_event'] = VolunteerAssignment.objects.filter(user=self.request.user)
        return context
    

class RejectedEventView(View):
    def get(self, request):
        context = {
            'rejected_event': VolunteerRequest.objects.filter(user=self.request.user, rejected=True).order_by("-requested_at"),
            'accepted_event': VolunteerRequest.objects.filter(user=self.request.user, accepted=True),
            'assign_event':VolunteerAssignment.objects.filter(user=self.request.user)
        }

        return render(request, 'profile/rejected_event_listing.html', context)
    
class AcceptedEventView(View):
    def get(self, request):
        context = {
            'rejected_event': VolunteerRequest.objects.filter(user=self.request.user, rejected=True),
            'accepted_event': VolunteerRequest.objects.filter(user=self.request.user, accepted=True).order_by("-requested_at"),
            'assign_event':VolunteerAssignment.objects.filter(user=self.request.user)
        }

        return render(request, 'profile/accepted_event_listing.html', context)
    
class AssignEventView(View):
    def get(self, request):
        context = {
            'rejected_event': VolunteerRequest.objects.filter(user=self.request.user, rejected=True),
            'accepted_event': VolunteerRequest.objects.filter(user=self.request.user, accepted=True),
            'assign_event':VolunteerAssignment.objects.filter(user=self.request.user).order_by("-assigned_at")
        }

        return render(request, 'profile/assign_event_listing.html', context)