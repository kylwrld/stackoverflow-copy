from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

class IsGetOrIsAuthenticated(JWTAuthentication):        
    def has_permission(self, request, view):        
        if request.method == 'GET':
            return True

        return request.user and request.user.is_authenticated