from rest_framework import serializers
from .models import TimeTracking
from baseapp.serializers import AutoAddUpdateBySerializer


class PostTimeTrackingSerializer(AutoAddUpdateBySerializer):

    class Meta:
        model = TimeTracking
        fields = '__all__'
