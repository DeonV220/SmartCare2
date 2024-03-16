from django.contrib.auth.backends import ModelBackend
from .models import OwnerProfile, OwnerProfileManager, OwnerProfileUser

class OwnerProfileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = OwnerProfileManager.objects.get(username=username)
        except OwnerProfileUser.DoesNotExist:
            return None
        

        if user.check_password(password):
            owner_profile = OwnerProfile.objects.filter(user=user).first()
        
            if owner_profile:
                return user

        return None