from django.contrib import admin
from .models import Event, VolunteerRequest, VolunteerAssignment
# Register your models here.

admin.site.register(Event)
admin.site.register(VolunteerRequest)
admin.site.register(VolunteerAssignment)