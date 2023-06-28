from rest_framework import serializers  
from .models import BaseModel
import uuid
import logging

class AutoAddUpdateBySerializer(serializers.ModelSerializer):
    """
    Auto add update_by serializers 
    """
    # def update(self, instance, data):
    #     instance = super().update(instance, data)
    #     instance.updated_by = self.context.get('request').user 
    #     instance.save()
    #     return instance
    pass 

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
    
class BulkUpdateSerializer(serializers.ModelSerializer):
    
    def validate_objects(self, objects):
        exist_ids = self.Meta.model.objects.all().values_list('id', flat = True)
        error_lst = []
        for obj in objects:
            if not (isinstance(obj, dict) and obj.get('id')):
                error_lst.append(f'{obj} is not valid')
            try : 
                id = uuid.UUID(obj.get('id')) 
            except Exception as e :
                error_lst.append(f"id {obj.get('id')} is not valid")
                continue
            if id not in exist_ids:
                error_lst.append(f"id {obj.get('id')} is not valid")
        if error_lst:
            raise serializers.ValidationError(error_lst)
        return objects