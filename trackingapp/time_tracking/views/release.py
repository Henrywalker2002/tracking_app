from .base_view_recycle import BaseViewRecycle
from time_tracking.models.release import Release
from time_tracking.serializers.release import ReadDetailReleaseSerializer, WriteReleaseSerializer, RecycleReleaseSerializer
from rest_framework.decorators import action
from time_tracking.models.time_tracking import TimeTracking
from rest_framework.response import Response
from time_tracking.custom_permission import TimeTrackingPermission
from time_tracking.filters.release import ReleaseFilter

class ReleaseModelViewSet(BaseViewRecycle):
    
    queryset = Release.objects.all()
    serializer_class = {"default" : WriteReleaseSerializer, "list" : ReadDetailReleaseSerializer, 
                        "retrieve" : ReadDetailReleaseSerializer, "restore" : RecycleReleaseSerializer, 
                        'get_item_deleted': ReadDetailReleaseSerializer}
    permission_classes = [TimeTrackingPermission]
    filterset_class = ReleaseFilter
    search_fields = ['@release', '@description']
