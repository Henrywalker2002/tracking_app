from .base_view_recycle import BaseViewRecycle
from time_tracking.models.release import Release
from time_tracking.serializers.release import WrirteReleaseSerializer
from rest_framework.decorators import action
from time_tracking.models.time_tracking import TimeTracking
from time_tracking.serializers.time_tracking import TimeTrackingSerializer
from rest_framework.response import Response


class ReleaseModelViewSet(BaseViewRecycle):
    
    queryset = Release.objects.all()
    serializer_class = {"default" : WrirteReleaseSerializer}
