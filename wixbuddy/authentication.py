from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from .models import AccessToken, User

class TokenAuthentication(BaseAuthentication):
    """
    Custom token authentication for AccessToken model
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token_value = auth_header.split(' ')[1]
        
        try:
            access_token = AccessToken.objects.get(token=token_value, is_active=True)
            
            # Check if token is expired
            if access_token.is_expired():
                access_token.is_active = False
                access_token.save()
                raise AuthenticationFailed('Access token has expired. Please sign in again.')
            
            return (access_token.user, access_token)
            
        except AccessToken.DoesNotExist:
            raise AuthenticationFailed('Invalid or expired token')
        except Exception as e:
            raise AuthenticationFailed(str(e))

class IsAuthenticated(BasePermission):
    """
    Custom permission class that checks if user is authenticated
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated 