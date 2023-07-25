from rest_framework import serializers
from time_tracking.models.release import Release
from django.db.models import Max, Min
from time_tracking.models.time_tracking import TimeTracking
from user.serializers import ReadSortUserSerializer


class WriteReleaseSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Release
        fields = ['release', 'start_time', 'end_time', 'status', 'description']

    def validate(self, data):
        start_time = data.get('start_time') or self.instance.start_time
        end_time = data.get('end_time') or self.instance.end_time
        if end_time < start_time:
            raise serializers.ValidationError(
                'end_time must be after start_time')
        if self.instance:
            dic = TimeTracking.objects.filter(
                release=self.instance).aggregate(Max('end_time'), Min('start_time'))
            if not dic.get('end_time__max') or not dic.get("start_time__min"):
                return data
            # raise more suitable error message
            error_lst = []
            if end_time < dic.get('end_time__max'):
                error_lst.append("end time must be later than all task")
            if start_time > dic.get('start_time__min'):
                error_lst.append("start time must be earlier than all task")
            if error_lst:
                raise serializers.ValidationError(error_lst)
        return data
    
class ReadSortReleaseSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Release
        exclude = ['is_deleted', 'updated_by', 'created_by']

class ReadDetailReleaseSerializer(ReadSortReleaseSerailizer):

    created_by = ReadSortUserSerializer(read_only= True)
    updated_by = ReadSortUserSerializer(read_only= True)
    
    class Meta:
        model = Release
        exclude = ['is_deleted']

class RecycleReleaseSerializer(serializers.ModelSerializer):
    
    ids = serializers.ListField(child = serializers.UUIDField())
    
    class Meta:
        model = Release
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