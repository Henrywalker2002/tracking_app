from rest_framework.permissions import BasePermission

class CustomPermission(BasePermission):
    """
    You have to impletament verify_permission(self, action, view) to use this class 
    """
    def verify_permisison(self , action, request, view):
        raise "Child of CustomPermisison must have verify_permission funcion"
    
    def has_permission(self, request, view):
        
        if not request.user.is_authenticated:
            return False
        
        permission_lst = request.user.permission_code_names
        
        for perm in permission_lst:
            if perm == "all":
                return True 
            else :
                appname, action = perm.split('.')
                if appname == view.basename:
                    if self.verify_permission(action, request, view):
                        return True
        
        return False