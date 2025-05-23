from django.contrib.auth.backends import ModelBackend
from userctl.models import UserInfo

class UserInfoBackend(ModelBackend):
    def authenticate(self, request, name=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get(name=name)
        except UserInfo.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
