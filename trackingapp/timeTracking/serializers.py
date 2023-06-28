from rest_framework import serializers
from .models import TimeTracking


class PostTimeTrackingSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeTracking
        fields = '__all__'
