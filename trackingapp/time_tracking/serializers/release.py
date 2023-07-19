from rest_framework import serializers
from time_tracking.models.release import Release
from django.db.models import Max, Min
from time_tracking.models.time_tracking import TimeTracking


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
    
class ReadReleaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Release
        fields = '__all__'