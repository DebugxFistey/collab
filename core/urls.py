from django.urls import path
from .views import Home, ContactView


urlpatterns = [
    path('', Home.as_view(), name='home'),
    # path('contact/', ContactView.as_view(), name='contact')
]