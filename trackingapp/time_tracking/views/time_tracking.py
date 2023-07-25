from time_tracking.models.time_tracking import TimeTracking
from time_tracking.models.history import History
from time_tracking.models.subcriber import Subcriber, SubcriberType
from time_tracking.serializers.time_tracking import (WriteTimeTrackingSerializer, ReadTimeTrackingDetailSerializer,
                                                     ReadTimeTrackingSummarySerializer, BulkDeleteTimeTrackingSerializer,
                                                     RecycleTimeTrackingSerializer)
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
from notification.models import Notification, TypeNotification
from notification.execute import add_notification_for_assign_task


class TimeTrackingViewSet(BaseViewRecycle):
    serializer_class = {"default": WriteTimeTrackingSerializer, "list" : ReadTimeTrackingSummarySerializer, 
                        "retrieve" : ReadTimeTrackingDetailSerializer, "bulk_delete" : BulkDeleteTimeTrackingSerializer,
                        'restore' : RecycleTimeTrackingSerializer, 'get_item_deleted': ReadTimeTrackingDetailSerializer}
    queryset = TimeTracking.objects.all() 
    permission_classes = [TimeTrackingPermission]
    filterset_class = TimeTrackingFilter
    search_fields = ['@task_id', '@user__first_name', '@user__last_name', '@release__release']
    
    def get_queryset(self):
        
        if self.action not in ["get_item_deleted", "restore"]:
            if self.action == "list":
                return self.queryset.filter(is_deleted= False).select_related('user').select_related('release')
            return self.queryset.filter(is_deleted= False)
        else :
            if self.action == "get_item_deleted":
                return self.queryset.filter(is_deleted= True).select_related('user').select_related('release')
            return self.queryset.filter(is_deleted= True)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        
        self.perform_create(serializer)
        instance = serializer.instance
        
        serializer_return = self.get_serializer(instance = instance, is_get = True)
        add_notification_for_assign_task(instance)
        
        headers = self.get_success_headers(serializer_return.data)
        return Response(data = serializer_return.data, headers= headers, status= status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """
        override to get change field 
        """
        current_time_tracking = self.get_object()
        old_instance = self.get_serializer(current_time_tracking, is_get = True).data
        response = super().update(request, *args, **kwargs)

        changed_time_tracking = self.get_object()
        if current_time_tracking.user != changed_time_tracking.user:
            add_notification_for_assign_task(self.get_object())
        
        new_instance = response.data
        process_history(current_time_tracking, old_instance, new_instance)
        return response

        