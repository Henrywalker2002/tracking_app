from base.base_permission import CustomPermission

class RolePermission(CustomPermission):
    def verify_permisison(self, action, request, view):
        return False
