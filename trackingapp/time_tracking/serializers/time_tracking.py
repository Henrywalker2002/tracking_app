from time_tracking.models.time_tracking import TimeTracking
from rest_framework import serializers
from base.serializers import BulkDeleteSerializer
from time_tracking.serializers.release import ReadSortReleaseSerailizer
from user.serializers import ReadSortUserSerializer

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
    
    user = ReadSortUserSerializer(read_only= True)
    release = ReadSortReleaseSerailizer(read_only= True)
    created_by = ReadSortUserSerializer(read_only= True)
    updated_by = ReadSortUserSerializer(read_only= True)
    
    class Meta:
        model = TimeTracking
        exclude = ['is_deleted']
        
class ReadTimeTrackingDetailSerializer(ReadTimeTrackingSummarySerializer):
    
    user = ReadSortUserSerializer(read_only= True)
    release = ReadSortReleaseSerailizer(read_only= True)
    
class BulkDeleteTimeTrackingSerializer(BulkDeleteSerializer):
    class Meta:
        model = TimeTracking
        fields = ['ids']

class RecycleTimeTrackingSerializer(serializers.ModelSerializer):
    
    ids = serializers.ListField(child = serializers.UUIDField())
    
    class Meta:
        model = TimeTracking
        fields = ['ids']
    
    def validate_ids(self, ids):

        if not isinstance(ids, list):
            raise serializers.ValidationError("ids must be a list")
        instance_lst = self.Meta.model.objects.filter(id__in = ids, is_deleted= True)
        validated_ids = instance_lst.values_list('id', flat = True)
        
        error_ids = []
        for id in ids : 
            if id not in validated_ids: 
                error_ids.append("id {} is not exist or is not deleted".format(id))
        if error_ids:
            raise serializers.ValidationError(error_ids)
        return instance_lst