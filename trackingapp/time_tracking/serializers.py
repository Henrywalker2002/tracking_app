from rest_framework import serializers
from .models import TimeTracking


class WriteTimeTrackingSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeTracking
        fields = '__all__'
        
    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        if end_time < start_time:
            raise serializers.ValidationError('end_time must be after start_time')
        return data
