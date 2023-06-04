from django.urls import path
from .views import UserProfileView, ProfilePictureUpdateView, PasswordChangeView, RejectedEventView, AcceptedEventView, AssignEventView, ProviderProfileView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('provider/profile/<int:pk>/', ProviderProfileView.as_view(), name='provider_detail'),
    path('change/profile_pic/', ProfilePictureUpdateView.as_view(), name='profile_pic_update'),
    path('change/password/', PasswordChangeView.as_view(), name='change_password'),
    path('rejected/event/', RejectedEventView.as_view(), name='rejected_event'),
    path('accepted/event/', AcceptedEventView.as_view(), name='accepted_event'),
    path('assign/event/', AssignEventView.as_view(), name='assign_event'),
]