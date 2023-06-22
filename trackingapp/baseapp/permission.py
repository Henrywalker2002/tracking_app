from rest_framework.permissions import BasePermission
from permissions.models import Role ,Permission 
from user.models import User

class CustomPermission(BasePermission):
    
    def has_permission(self, request, view):
        return True