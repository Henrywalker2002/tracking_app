from base.base_permission import CustomPermission

class NotificationPermission(CustomPermission):

    def verify_permission(self, action, request, view):
        user_id = request.query_params.get('id', None)
        if user_id:
            return str(request.user.id) == user_id
        return True
    
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id 