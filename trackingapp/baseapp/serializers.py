from rest_framework import serializers  
from .models import BaseModel
import logging

class AutoAddUpdateBySerializer(serializers.ModelSerializer):
    """
    Auto add update_by serializers 
    """
    
    def update(self, instance, data):
        instance = super().update(instance, data)
        instance.updated_by = self.context.get('request').user 
        instance.save()
        return instance
    
class BulkDeleteSerializer(serializers.ModelSerializer):
    """
    Serilizer for bulk delete and bulk edit, validate ids. 
    Must have class Meta have fields = ['ids']
    """
    ids = serializers.ListField(child = serializers.UUIDField())
        
    def validate_ids(self, ids):
        logging.info('{} begin validate_ids on bulk'.format(self.context['request']._request.content_params.get('id')))
        if not isinstance(ids, list):
            raise serializers.ValidationError("ids must be a list")
        validated_ids = self.Meta.model.objects.filter(id__in = ids).values_list('id', flat = True)
        error_ids = []
        for id in ids : 
            if id not in validated_ids: 
                error_ids.append("id {} is not exist".format(id))
        if error_ids:
            raise serializers.ValidationError(error_ids)
        logging.info('{} end validate_ids on bulk'.format(self.context['request']._request.content_params.get('id')))
        return ids