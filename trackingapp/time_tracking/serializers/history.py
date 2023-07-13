from rest_framework import serializers
from base.decorators import query_debugger
from django.core.cache import cache
from user.models import User
from time_tracking.models.history import History
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject
from rest_framework.fields import SkipField


class ReadHistorySerializer(serializers.ModelSerializer):

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
                    if attribute.get('user'):
                        new_value = get_email(attribute.get('user').get('new_value'))
                        old_value = get_email(attribute.get('user').get('old_value'))
                        attribute['user'] = {"new_value" : new_value, "old_value" : old_value}
                        attribute['user_email'] = attribute.pop('user')
                ret[field.field_name] = field.to_representation(attribute)
        return ret