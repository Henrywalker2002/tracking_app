from .serializers import PostTimeTrackingSerializer
from .models import TimeTracking
from base.views import CustomModelViewSetBase
from rest_framework import permissions


class TimeTrackingViewSet(CustomModelViewSetBase):
    serializer_class = {"create": PostTimeTrackingSerializer, "update": PostTimeTrackingSerializer,
                        "partial": PostTimeTrackingSerializer, "default": PostTimeTrackingSerializer}
    queryset = TimeTracking.objects.all()
    permission_classes = [permissions.IsAuthenticated]
