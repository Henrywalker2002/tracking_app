from .serializers import WriteTimeTrackingSerializer
from .models import TimeTracking
from base.views import CustomModelViewSetBase
from rest_framework import permissions


class TimeTrackingViewSet(CustomModelViewSetBase):
    serializer_class = {"create": WriteTimeTrackingSerializer, "update": WriteTimeTrackingSerializer,
                        "partial": WriteTimeTrackingSerializer, "default": WriteTimeTrackingSerializer}
    queryset = TimeTracking.objects.all()
    permission_classes = [permissions.IsAuthenticated]
