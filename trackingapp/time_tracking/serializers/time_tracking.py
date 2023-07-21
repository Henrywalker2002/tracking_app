from time_tracking.models.time_tracking import TimeTracking
from rest_framework import serializers
from base.serializers import BulkDeleteSerializer
from time_tracking.serializers.release import ReadReleaseSerializer
from user.serializers import ReadUserSummarySerializer

class WriteTimeTrackingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TimeTracking
        fields = ["task_id", "task_link", "start_time", "end_time", "status", "user", "release"]

    def validate(self, data):
        start_time = data.get('start_time') or self.instance.start_time
        end_time = data.get('end_time') or self.instance.end_time
        if end_time < start_time:
            raise serializers.ValidationError(
                'end_time must be after start_time')

        release = data.get('release') or self.instance.release
        error_lst = []
        if start_time < release.start_time: 
            error_lst.append("start time of task must be earlier than start time of release")
        if end_time > release.end_time: 
            error_lst.append("end time of task must be later than end time of release")
        if error_lst:
            raise serializers.ValidationError(error_lst)
        return data
    
class ReadTimeTrackingSummarySerializer(serializers.ModelSerializer):
    
    user = serializers.SlugRelatedField(read_only= True, slug_field= "email")
    release = serializers.SlugRelatedField(read_only= True, slug_field= "release")
    
    class Meta:
        model = TimeTracking
        fields = '__all__'
        
class ReadTimeTrackingDetailSerializer(ReadTimeTrackingSummarySerializer):
    
    user = ReadUserSummarySerializer(read_only= True)
    release = ReadReleaseSerializer(read_only= True)
    
class BulkDeleteTimeTrackingSerializer(BulkDeleteSerializer):
    class Meta:
        model = TimeTracking
        fields = ['ids']
