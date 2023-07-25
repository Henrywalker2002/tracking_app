from rest_framework import serializers
from time_tracking.models.subcriber import Subcriber, SubcriberType
from time_tracking.models.time_tracking import TimeTracking
from time_tracking.models.release import Release
from user.serializers import ReadSortUserSerializer
from time_tracking.serializers.time_tracking import ReadTimeTrackingSummarySerializer
from time_tracking.serializers.release import ReadSortReleaseSerailizer

class WriteSubcriberSerializer(serializers.ModelSerializer):
    
    id = serializers.UUIDField(read_only= True)
    time_tracking = serializers.PrimaryKeyRelatedField(required= False, queryset = TimeTracking.objects.all())
    release = serializers.PrimaryKeyRelatedField(required= False, queryset = Release.objects.all())
    
    class Meta:
        model = Subcriber
        fields = ['id', 'user', 'time_tracking', 'release', 'object_type']

    def validate(self, data):
        type = data.get('object_type')
        if type == SubcriberType.RELEASE:
            if not data.get('release'):
                raise serializers.ValidationError(f"object_type = {SubcriberType.RELEASE} must have field release")
            instance = self.Meta.model.objects.filter(release= data.get('release'), 
                                                      user= data.get('user'), object_type= SubcriberType.RELEASE)
            if instance:
                raise serializers.ValidationError(
                    f"user '{data.get('user')}' have already subcribed to release '{data.get('release')}'")
        else :
            if not data.get('time_tracking'):
                raise serializers.ValidationError(f"object_type = {SubcriberType.TASK} must have field time_tracking")
            instance = self.Meta.model.objects.filter(
                time_tracking=data.get('time_tracking'), user=data.get('user'), object_type= SubcriberType.TASK)
            if instance:
                raise serializers.ValidationError(
                    f"user {data.get('user')} have already subcribed to time tracking {data.get('time_tracking')}")
        return data
    
class ReadSubcriberSerializer(serializers.ModelSerializer):
    
    user = ReadSortUserSerializer(read_only= True)
    time_tracking = ReadTimeTrackingSummarySerializer(read_only=True)
    release = ReadSortReleaseSerailizer(read_only= True)
    
    class Meta:
        model = Subcriber
        exclude = ['created_by', 'updated_by']