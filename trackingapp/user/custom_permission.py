from rest_framework.permissions import BasePermission
from base.base_permission import CustomPermission
from user.models import User

class UserPermission(CustomPermission):
    
    def verify_permission(self, action,request, view):
        if view.detail and action == "self":
            return True 
        if view.action == action:
            return True
    
    def has_object_permission(self, request, view,obj):
        permission_lst = request.user.permission_code_names
        all_perm = False
        for perm in permission_lst:
            if perm == "all":
                all_perm = True
                
        if all_perm:
            return True
        
        if isinstance(obj, User):
            if view.action in ["update_role", "delete_role"]:
                return False
            return request.user.id == obj.id 
        return False

