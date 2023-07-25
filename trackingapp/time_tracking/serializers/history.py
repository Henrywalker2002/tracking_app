from rest_framework import serializers
from base.decorators import query_debugger
from user.models import User
from time_tracking.models.history import History
from time_tracking.models.release import Release
from time_tracking.serializers.time_tracking import ReadTimeTrackingSummarySerializer
from time_tracking.serializers.release import ReadSortReleaseSerailizer
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject
from rest_framework.fields import SkipField
from user.serializers import ReadSortUserSerializer


class HistorySummarySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = History
        exclude = ['created_by', 'updated_by']
        
    def get_user(self, id):
        instance = User.objects.filter(id = id)
        if instance:
            return ReadSortUserSerializer(instance.get()).data
        return None
    
    def get_release(self, id):
        instance = Release.objects.filter(id = id)
        if instance:
            return ReadSortReleaseSerailizer(instance.get()).data
        return None
         
        
    def to_representation(self, instance):
        """
        custom to represent user email instead of user id 
        """
        ret = super().to_representation(instance)
        
        change_detection = ret.get('change_detection')
        if not change_detection:
            return ret
        if 'user' in change_detection.keys():
            change_detection['user']['old_value'] = self.get_user(change_detection['user'].get('old_value'))
            change_detection['user']['new_value'] = self.get_user(change_detection['user'].get('new_value'))
        if 'release' in change_detection.keys():
            change_detection['release']['old_value'] = self.get_release(change_detection['release'].get('old_value'))
            change_detection['release']['new_value'] = self.get_release(change_detection['release'].get('new_value'))
        ret['change_detection'] = change_detection
        
        return ret

class HistoryDetailSerializer(HistorySummarySerializer):
    """
    Get more detail for time_tracking
    """
    time_tracking = ReadTimeTrackingSummarySerializer(read_only= True)
        

        