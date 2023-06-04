from django.urls import path
from events.views import EventCreateView, event_detail, VolunteerRequestView, SearchView, VolunteerRequestListView, AssignVolunteerView, RejectedVolunteerView, VolunteerAssignedListView,RemoveAssignVolunteerView, VolunteerRejectedListView, EventListView, EventDetailView, EventListsView

urlpatterns = [
    path('provider/create_event/', EventCreateView.as_view(), name='create_event'),
    path('provider/event/list/', EventListView.as_view(), name='event_list'),
    path('provider/event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('provider/request_list/', VolunteerRequestListView.as_view(), name='request_list'),
    path('provider/assign_list/', VolunteerAssignedListView.as_view(), name='assign_list'),
    path('provider/reject_list/', VolunteerRejectedListView.as_view(), name='reject_list'),
    path('provider/assign/process/', AssignVolunteerView.as_view(), name='assign_process'),
    path('provider/reject/process/', RejectedVolunteerView.as_view(), name='reject_process'),
    path('provider/remove/assign/process/', RemoveAssignVolunteerView.as_view(), name='remove_assign_process'),
    
    
    path('event_detail/<int:event_id>/', event_detail, name='event_detail'),
    path('volunteer_request/ajax/', VolunteerRequestView.as_view(), name='volunteer_request'),
    path('search/', SearchView.as_view(), name='search'),
    path('list/', EventListsView.as_view(), name='list'),
]