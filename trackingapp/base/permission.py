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
                    if view.action == action:
                        if view.detail:
                            if view.kwargs.get('pk') == str(request.user.id):
                                return True
                        else :
                            return True
                
                elif view.basename in ['timetracking', 'notification']:
                    if action == 'all':
                        return True
                    else :
                        if view.detail and view.kwargs.get('pk') == request.user.id:
                            return True
                        if request.user.id == request.GET.get('id'):
                            return True
                elif view.basename == "subcriber":
                    return True
        return False
