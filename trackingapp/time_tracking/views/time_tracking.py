from time_tracking.models.time_tracking import TimeTracking
from time_tracking.models.history import History
from time_tracking.models.subcriber import Subcriber, SubcriberType
from time_tracking.serializers.time_tracking import WriteTimeTrackingSerializer, ListTimeTrackingSerializer,RetrieveTimeTrackingSerializer, BulkDeleteTimeTrackingSerializer
from django.db import transaction
from .base_view_recycle import BaseViewRecycle
from rest_framework.response import Response
from base.decorators import query_debugger
from rest_framework.decorators import action
from rest_framework import status
from notification.execute import add_notification_for_history_change
from time_tracking.custom_permission import TimeTrackingPermission
from time_tracking.execute import process_history
from time_tracking.filters.time_tracking import TimeTrackingFilter


class TimeTrackingViewSet(BaseViewRecycle):
    serializer_class = {"default": WriteTimeTrackingSerializer, "list" : ListTimeTrackingSerializer, 
                        "retrieve" : RetrieveTimeTrackingSerializer, "bulk_delete" : BulkDeleteTimeTrackingSerializer}
    queryset = TimeTracking.objects.all()
    permission_classes = [TimeTrackingPermission]
    filterset_class = TimeTrackingFilter
    
    def get_queryset(self):
        
        if self.action not in ["get_item_deleted", "restore"]:
            if self.action == "list":
                return self.queryset.filter(is_deleted= False).select_related('user').select_related('release')
            return self.queryset.filter(is_deleted= False)
        else :
            if self.action == "get_item_deleted":
                return self.queryset.filter(is_deleted= True).select_related('user').select_related('release')
            return self.queryset.filter(is_deleted= True)
    
    
    def update(self, request, *args, **kwargs):
        """
        override to get change field 
        """
        current_time_tracking = self.get_object()
        old_instance = self.get_serializer(current_time_tracking, is_get = True).data
        response = super().update(request, *args, **kwargs)
        new_instance = response.data
        process_history(current_time_tracking, old_instance, new_instance)
        return response

        