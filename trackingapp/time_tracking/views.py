from time_tracking.serializers import WriteTimeTrackingSerializer, ViewHistorySerializer, SubcriberSerializer
from time_tracking.models import TimeTracking, History, Subcriber
from base.views import BulkActionBaseModelViewSet
from rest_framework import permissions
from django.db import transaction
from uuid import UUID
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, mixins
import threading
from notification.views import proccess_history_change
from trackingapp.custom_middleware import CustomThread

class TimeTrackingViewSet(BulkActionBaseModelViewSet):
    serializer_class = {"create": WriteTimeTrackingSerializer, "update": WriteTimeTrackingSerializer,
                        "partial": WriteTimeTrackingSerializer, "default": WriteTimeTrackingSerializer}
    queryset = TimeTracking.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        current_time_tracking = self.get_object()
        old_instance = self.get_serializer(current_time_tracking).data
        response = super().update(request, *args, **kwargs)
        new_instance = response.data
        excluded_fields = ['id', 'created_at', 'modified_at', 'created_by']
        change_lst = {}
        for key in old_instance.keys():
            if key in excluded_fields:
                continue
            if old_instance[key] != new_instance[key]:
                change_lst[key] = {"old_value": str(
                    old_instance[key]), "new_value": str(new_instance[key])}
        history_data = {"time_tracking": current_time_tracking,
                        "user": request.user, "change_detection": change_lst}
        if change_lst:
            history_instance = History.objects.create(**history_data)
            thread = CustomThread(target= proccess_history_change, args=(history_instance, request.user))
            thread.start()
        return response
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_deleted:
            instance.delete()
            return Response
        thread = threading.Thread(target= instance.delete, args=())
        thread.start()
        return Response(status= status.HTTP_204_NO_CONTENT) 

class BaseView: 
    
    @action(detail= False, url_path="get-by-user-id")
    def get_by_user_id(self, request):
        param = request.GET 
        try: 
            id = UUID(param.get('id'))
            instance_lst = self.get_queryset().filter(user_id = id)
            serializer = self.get_serializer(instance_lst, many = True)
            return Response(serializer.data)
        except ValueError as e:
            return Response(data={"id": f"id {param.get('id')} is not valid"}, status=400)
        
    @action(detail= False, url_path= "get-by-time-tracking-id")
    def get_by_time_tracking_id(self, request):
        param = request.GET
        try:
            id = UUID(param.get('id'))
            instance_lst = self.get_queryset().filter(time_tracking_id=id)
            serializer = self.get_serializer(instance_lst, many=True)
            return Response(serializer.data)
        except ValueError as e:
            return Response(data={"id": f"id {param.get('id')} is not valid"}, status=400)

class HistoryViewOnly(ReadOnlyModelViewSet, BaseView):
    serializer_class = ViewHistorySerializer
    queryset = History.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class SubcriberModelViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin, BaseView):
    """
    Only need create and detele
    """
    serializer_class = SubcriberSerializer
    queryset = Subcriber.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    