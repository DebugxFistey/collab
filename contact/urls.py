import imp
from django.urls import path
from . import views

app_name = "contact"

urlpatterns = [
    path('form/',views.ContactFormView.as_view(),name = "contact"),
]