from rest_framework import serializers
from time_tracking.models import TimeTracking, History, Subcriber
import uuid
from django.core.cache import cache
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject
from user.models import User 
from base.decorators import query_debugger

class WriteTimeTrackingSerializer(serializers.ModelSerializer):
    
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


class ViewHistorySerializer(serializers.ModelSerializer):

    email_user = serializers.CharField(read_only= True)
    email_updated_by = serializers.CharField(read_only= True)
    email_created_by = serializers.CharField(read_only= True)
    
    class Meta:
        model = History
        fields = '__all__'
        
    def to_representation(self, instance):
        """
        custom to represent user email instead of user id 
        """
        @query_debugger
        def get_email(id):
            if cache.get(id):
                return cache.get(id)
            try :
                return cache.get_or_set(id, User.objects.get(id =id).email or None)
            except User.DoesNotExist as e:
                return None
        
        ret = OrderedDict()
        fields = self._readable_fields
        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                if field.field_name == "change_detection":
                    if attribute.get('user_id'):
                        new_value = get_email(attribute.get('user_id').get('new_value'))
                        old_value = get_email(attribute.get('user_id').get('old_value'))
                        attribute['user_id'] = {"new_value" : new_value, "old_value" : old_value}
                        attribute['user_email'] = attribute.pop('user_id')
                ret[field.field_name] = field.to_representation(attribute)
        return ret


class SubcriberSerializer(serializers.ModelSerializer):
    
    email_user = serializers.CharField(read_only= True) 

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