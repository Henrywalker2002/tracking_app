from .base_view_recycle import BaseViewRecycle
from time_tracking.models.release import Release
from time_tracking.serializers.release import ReadReleaseSerializer, WriteReleaseSerializer
from rest_framework.decorators import action
from time_tracking.models.time_tracking import TimeTracking
from rest_framework.response import Response
from time_tracking.custom_permission import TimeTrackingPermission

class ReleaseModelViewSet(BaseViewRecycle):
    
    queryset = Release.objects.all()
    serializer_class = {"default" : WriteReleaseSerializer, "list" : ReadReleaseSerializer, 
                        "retrieve" : ReadReleaseSerializer}
    permission_classes = [TimeTrackingPermission]
