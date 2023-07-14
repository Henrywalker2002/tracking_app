from rest_framework.permissions import BasePermission
from permissions.models import Role, Permission
from time_tracking.models.subcriber import Subcriber
from media.models import Media
from user.models import User
from functools import reduce

class CustomPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # perm_lst get from authenticate of custom authentication
        permission_lst = request.user.permission_code_names
        
        for perm in permission_lst:
            if perm == 'all':
                return True
            else: 
                appname, action = perm.split('.')
                if view.basename == "user" and appname == "user":
                    if view.detail and action == "self":
                        return True 
                    if view.action == action:
                        return True
                elif view.basename in ["timetracking", "history", "notification", 'release'] and appname == view.basename:
                    if action == "all" or request.method == "GET":
                        return True   
                elif view.basename == "subcriber" and appname == "subcriber":
                    return True 
                elif view.basename == "media" and appname == "media":
                    return True 
        return False
    
    def has_object_permission(self, request, view,obj):
        permission_lst = request.user.permission_code_names
        all_perm = False
        for perm in permission_lst:
            if perm == "all":
                all_perm = True
                
        if all_perm:
            return True

        if isinstance(obj, Media):
            return request.user.id == obj.created_by 
        elif isinstance(obj, Subcriber):
            return request.user.id == obj.user_id
        elif isinstance(obj, User):
            if view.action in ["update_role", "delete_role"]:
                return False
            return request.user.id == obj.id 
        return True
