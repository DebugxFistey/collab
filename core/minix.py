from django.contrib.auth.mixins import UserPassesTestMixin

class VolunteerRequestPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_volunteer
    
class ProviderRequestPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_provider
