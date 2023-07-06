from rest_framework.permissions import BasePermission
from permissions.models import Role, Permission
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
                if view.basename == 'user':
                    if role == "admin" :
                        if view.action == action:
                            return True
                    else :
                        if view.detail:
                            if str(request.user.id) == (view.kwargs.get('pk') or ' '):
                                return True
                elif view.basename == "timetracking":
                    if action == 'all':
                        return True
                    else :
                        return view.action == action
                elif view.basename == "subcriber":
                    return True 
                elif view.basename == "notification":
                    return True
        return False
