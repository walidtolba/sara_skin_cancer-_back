from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from users.models import User
import jwt


class JSONWebTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            payload = jwt.decode(key, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(email=payload['email'])
        except (jwt.DecodeError, User.DoesNotExist):
            raise exceptions.AuthenticationFailed('Invalid token')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')
        return (user, payload)