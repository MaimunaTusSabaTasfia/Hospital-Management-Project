from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """Authenticate using either username or email."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return None

        username = username.strip()

        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            # Try matching first_name + last_name as full name
            name_parts = username.split()
            if len(name_parts) >= 2:
                first_name = name_parts[0]
                last_name = ' '.join(name_parts[1:])
                try:
                    user = UserModel.objects.get(
                        Q(first_name__iexact=first_name, last_name__iexact=last_name)
                    )
                except UserModel.DoesNotExist:
                    return None
            else:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
