from time_tracking.models.time_tracking import TimeTracking
from rest_framework import serializers

class TimeTrackingSerializer(serializers.ModelSerializer):
    
    email_updated_by = serializers.CharField(read_only= True)
    email_created_by = serializers.CharField(read_only= True)
    email_user = serializers.CharField(read_only= True)
    
    class Meta:
        model = TimeTracking
        fields = '__all__'

    def validate(self, data):
        start_time = data.get('start_time') or self.instance.start_time
        end_time = data.get('end_time') or self.instance.end_time
        if end_time < start_time:
            raise serializers.ValidationError(
                'end_time must be after start_time')
        return data