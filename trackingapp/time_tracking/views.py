from time_tracking.serializers import WriteTimeTrackingSerializer, ViewHistorySerializer, SubcriberSerializer
from time_tracking.models import TimeTracking, History, Subcriber
from base.views import BulkActionBaseModelViewSet, GetByTimeTrackingIdMixin, GetByUserIdMixin
from django.db import transaction
from django.db.models.query import QuerySet
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, mixins, serializers, permissions
from uuid import UUID

from trackingapp.custom_middleware import CustomThread

class TimeTrackingViewSet(BulkActionBaseModelViewSet):
    serializer_class = {"create": WriteTimeTrackingSerializer, "update": WriteTimeTrackingSerializer,
                        "partial": WriteTimeTrackingSerializer, "default": WriteTimeTrackingSerializer}
    queryset = TimeTracking.objects.all()
    
    def get_queryset(self):
        """
        Override to get only instance which is_deleted is False 
        """
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            if self.action not in ["get_time_tracking_deleted", "restore"]:
                queryset = queryset.filter(is_deleted= False)
            else :
                queryset = queryset.filter(is_deleted= True)
        return queryset
    

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        
        from notification.views import proccess_history_change
        
        current_time_tracking = self.get_object()
        old_instance = self.get_serializer(current_time_tracking).data
        response = super().update(request, *args, **kwargs)
        new_instance = response.data
        excluded_fields = ['id', 'created_at', 'modified_at', 'created_by', 'updated_by']
        change_lst = {}
        for key in old_instance.keys():
            if key in excluded_fields:
                continue
            if old_instance[key] != new_instance[key]:
                # remove old subcriber 
                if key == 'user':
                    subcriber_instance = Subcriber.objects.filter(user_id = old_instance.get('user'), 
                                                                  time_tracking_id = old_instance.get('id'))
                    if subcriber_instance:
                        subcriber_instance.delete()
    
                change_lst[key] = {"old_value": str(
                    old_instance[key]), "new_value": str(new_instance[key])}
        history_data = {"time_tracking": current_time_tracking,
                        "user": request.user, "change_detection": change_lst}
        if change_lst:
            history_instance = History.objects.create(**history_data)
            # process history in background 
            proccess_history_change(history_instance)
        return response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_deleted:
            setattr(instance, 'is_deleted', True)
            instance.save()
        return Response(status= status.HTTP_204_NO_CONTENT) 

    @action(detail= False, url_path = 'recycle')
    def get_time_tracking_deleted(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail= True, url_path= 'recycle', methods=['put'])
    def restore(self, request, pk):
        instance = self.get_object()
        instance.is_deleted = False
        instance.save()
        return Response(status= status.HTTP_204_NO_CONTENT)
        
class HistoryViewOnly(GenericViewSet, mixins.RetrieveModelMixin, GetByTimeTrackingIdMixin, GetByUserIdMixin):
    serializer_class = ViewHistorySerializer
    queryset = History.objects.all()


class SubcriberModelViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                            GetByTimeTrackingIdMixin, GetByUserIdMixin):
    """
    Only need get, create and detele
    """
    serializer_class = SubcriberSerializer
    queryset = Subcriber.objects.all()
    