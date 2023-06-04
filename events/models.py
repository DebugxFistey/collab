from django.db import models
from taggit.managers import TaggableManager
from location_field.models.plain import PlainLocationField
from django.utils import timezone


from users.models import User

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    start_time = models.TimeField(default=timezone.now())
    end_time = models.TimeField(default=timezone.now())
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    max_volunteers = models.PositiveIntegerField()
    is_cancelled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    registration_start_date = models.DateTimeField()
    registration_end_date = models.DateTimeField()
    organizer_name = models.CharField(max_length=100)
    organizer_email = models.EmailField(max_length=254)
    organizer_phone = models.CharField(max_length=20)
    skills_required = TaggableManager()
    category_on = models.TextField()
    
    # def volunteer_request(self):
    #     return VolunteerRequest.objects.get(event__id=self.id)
    
    def available_volunteer(self):
        return self.max_volunteers - VolunteerRequest.objects.filter(event__id=self.id, accepted=True).count()


class VolunteerAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

class VolunteerRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
