from base.base_permission import CustomPermission
from time_tracking.models.subcriber import Subcriber


class TimeTrackingPermission(CustomPermission):
    
    def verify_permission(self, action, request, view):
        if view.basename == "subscriber":
            if request.method == "POST":
                user_id = request.data.get('user', None)
                return str(request.user.id) == user_id
            return True
        
        if action == "all" or request.method == "GET":
            return True        

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Subcriber):
            return obj.user_id == request.user.id 
        return True