from time_tracking.models.time_tracking import TimeTracking
from time_tracking.models.history import History
from time_tracking.models.subcriber import Subcriber, SubcriberType
from time_tracking.serializers.time_tracking import WriteTimeTrackingSerializer, ReadTimeTrackingSerializer, BulkDeleteTimeTrackingSerializer
from django.db import transaction
from .base_view_recycle import BaseViewRecycle
from rest_framework.response import Response
from base.decorators import query_debugger
from rest_framework.decorators import action
from rest_framework import status
from notification.execute import add_notification_for_history_change
from time_tracking.custom_permission import TimeTrackingPermission


class TimeTrackingViewSet(BaseViewRecycle):
    serializer_class = {"default": WriteTimeTrackingSerializer, "list" : ReadTimeTrackingSerializer, 
                        "retrieve" : ReadTimeTrackingSerializer, "bulk_delete" : BulkDeleteTimeTrackingSerializer}
    queryset = TimeTracking.objects.all()
    permission_classes = [TimeTrackingPermission]
    
    def get_queryset(self):
        if self.action not in ["get_item_deleted", "restore"]:
            if self.action == "list":
                return self.queryset.filter(is_deleted= False).select_related('user').select_related('release')
            return self.queryset.filter(is_deleted= False)
        else :
            if self.action == "get_item_deleted":
                return self.queryset.filter(is_deleted= True).select_related('user').select_related('release')
            return self.queryset.filter(is_deleted= True)
    
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        override to get change field 
        """
        current_time_tracking = self.get_object()
        old_instance = self.get_serializer(current_time_tracking).data
        response = super().update(request, *args, **kwargs)
        new_instance = response.data
        excluded_fields = ['id', 'created_at',
                           'modified_at', 'created_by', 'updated_by', "email_user"]
        change_lst = {}
        for key in old_instance.keys():
            if key in excluded_fields:
                continue
            if old_instance[key] != new_instance[key]:
                # remove old subcriber
                if key == 'user':
                    subcriber_instance = Subcriber.objects.filter(user_id=old_instance.get('user'), 
                                        time_tracking_id=old_instance.get('id'), object_type = SubcriberType.TASK)
                    if subcriber_instance:
                        subcriber_instance.delete()

                change_lst[key] = {"old_value": str(
                    old_instance[key]), "new_value": str(new_instance[key])}
        history_data = {"time_tracking": current_time_tracking,
                        "change_detection": change_lst}
        if change_lst:
            history_instance = History.objects.create(**history_data)
            # process history in background
            add_notification_for_history_change(history_instance)
        return response

    
    @action(detail= False, url_path= "get-time-tracking-by-release-id")
    def get_time_tracking_by_release_id(self, request):
        param = request.GET
        release_id = param.get('release_id')
        if not release_id:
            return Response('release_id must be a param', status= status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(release_id = release_id)
        page = self.paginate_queryset(queryset)
        
        if page:
            serializer = self.get_serializer(page, many = True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data)
        