from rest_framework import serializers
from time_tracking.models import TimeTracking, History, Subcriber
import uuid


class WriteTimeTrackingSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeTracking
        fields = '__all__'

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        if end_time < start_time:
            raise serializers.ValidationError(
                'end_time must be after start_time')
        return data


class ViewHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'


class SubcriberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcriber
        fields = '__all__'

    def validate(self, data):
        instance = self.Meta.model.objects.filter(
            time_tracking=data.get('time_tracking'), user=data.get('user'))
        if instance:
            raise serializers.ValidationError(
                f"user {data.get('user')} have already subcribed to time tracking {data.get('time_tracking')}")
        return data
