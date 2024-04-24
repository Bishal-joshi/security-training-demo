from rest_framework.permissions import BasePermission
import jwt
from django.conf import settings
from authentication.models import User


def verify_and_decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Handle token expiration
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token
        return None


class CustomJWTAuthentication(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('Authorization')
        if not token:
            return False

        # Extract the token from the Authorization header (e.g., "Bearer <token>")
        # Modify this if your token format is different
        token = token.split(' ')[1] if token.startswith('Bearer') else token

        # Verify and decode the token
        payload = verify_and_decode_jwt(token)

        # Check if the token is valid and not expired
        if payload:
            # You can perform additional checks here if needed
            user_id = payload['user_id']
            request.user = User.objects.get(id=user_id)
            return True
        else:
            return False
