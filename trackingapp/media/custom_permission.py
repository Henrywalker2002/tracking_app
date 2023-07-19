from base.base_permission import CustomPermission

class MediaPermission(CustomPermission):

    def verify_permission(self, action, request, view):
        return True