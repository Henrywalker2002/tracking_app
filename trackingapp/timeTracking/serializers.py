from rest_framework import serializers
from .models import TimeTracking
from baseapp.serializers import AutoAddCreateBySerializer


class PostTimeTrackingSerializer(AutoAddCreateBySerializer):

    class Meta:
        model = TimeTracking
        fields = '__all__'
