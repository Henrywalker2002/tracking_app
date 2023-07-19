from rest_framework import serializers
from notification.models import Notification
from time_tracking.serializers.history import ReadHistorySerializer
from time_tracking.models.history import History
from time_tracking.models.time_tracking import TimeTracking
from time_tracking.serializers.time_tracking import ReadTimeTrackingSerializer


class ReadNotificationSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Notification
        fields = '__all__'
        
    def to_representation(self, instance):
        """
        Custom to view all history instead of history id 
        """
        ret = super().to_representation(instance)
        if ret.get('type') == "TIME_TRACKING_HISTORY":
            instance = History.objects.filter(id = ret.get('object_id'))
            if not instance:
                ret['history'] = None 
            else :
                ret['history'] = ReadHistorySerializer(instance=instance.get()).data
        else:
            instance = TimeTracking.objects.filter(id = ret.get('object_id'))
            if not instance:
                ret['time_tracking'] = None 
            else :
                ret['time_tracking'] = ReadTimeTrackingSerializer(instance.get()).data 
                
        return ret