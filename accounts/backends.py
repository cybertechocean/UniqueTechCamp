from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend allowing clients to log in using either
    their registered username OR their email address (case-insensitive) along with their password.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if not username or not password:
            return None

        # Clean whitespace
        username = username.strip()

        try:
            # Query by case-insensitive username or email
            user = User.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            ).order_by('id').first()

            if user and user.check_password(password):
                return user
        except Exception:
            return None

        return None
