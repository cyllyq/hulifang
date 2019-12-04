from django.contrib.auth.backends import ModelBackend
from users.models import User


class MobileBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(mobile=username, is_active=True)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None