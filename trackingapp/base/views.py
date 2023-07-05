from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
import logging
from functools import reduce
import uuid
import datetime
from django.utils import timezone

class CustomModelViewSetBase(viewsets.ModelViewSet):
    """
    custom get serializer class to get serializer class base on dict only
    """
    serializer_class = {}
    def get_serializer_class(self):
        if self.action in self.serializer_class.keys():
            return self.serializer_class[self.action]
        return self.serializer_class['default']
    
    def add_serilizer_class(self, key: str, value):
        """
        key is action name , value is serializer class. Example : add_serializer_class("create", PostSerializer)
        """
        self.serializer_class.update({key, value})
        
class BulkCreateMixin:
    
    def _bulk_create(self, data, user = None): 
        serializer = self.get_serializer(data = data, many = True)
        serializer.is_valid(raise_exception = True)
        instance_lst = []
        for obj in serializer.data:
            instance = self.get_serializer_class().Meta.model(**obj)
            if hasattr(instance, 'created_by'):
                setattr(instance, 'created_by', user)
            instance_lst.append(instance)
        self.get_serializer_class().Meta.model.objects.bulk_create(instance_lst)
        return serializer
    
    @action(methods= ['POST'], detail= False , url_path= 'bulk-create')
    def bulk_create(self, request):
        serializer = self._bulk_create(request.data, request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class BulkActionBaseModelViewSet(CustomModelViewSetBase, BulkCreateMixin):
    """
    Custom get serializer class to get serializer class base on dict 
    Bulk update, bulk detele, bulk create for perrmision and roles, time tracking
    """
        
    @action(methods= ['delete'], detail= False, url_path= 'bulk-delete')
    def bulk_delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        queryset.filter(id__in = serializer.data['ids']).delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    
    @action(methods=['PUT'], detail=False, url_path='bulk-update')
    def bulk_update(self, request, *args, **kwargs):
        """
        Update field pass by request.body['objects'] + updated_by 
        """
        instance_lst = []
        fields = {'updated_by', 'modified_at'}
            
        for obj in request.data:
            
            try :
                instance = self.get_queryset().get(id = obj.get('id'))
            except Exception as e:
                raise serializers.ValidationError(f"id {obj.get('id')} is not exist")
            
            serializer = self.get_serializer(instance ,data = obj)
            serializer.is_valid(raise_exception = True)
            
            for key,value in obj.items():
                # if in 4 field auto add, skip 
                if key in ['updated_by', 'modified_at', 'created_by', 'created_at', 'id']:
                    continue
                setattr(instance, key, value)
                fields.add(key)
            setattr(instance, 'updated_by', self.request.user)
            setattr(instance, 'modified_at', datetime.datetime.now(tz = timezone.utc))
            instance_lst.append(instance)
        self.get_serializer_class().Meta.model.objects.bulk_update(instance_lst, fields)
        return_serializer = self.get_serializer(instance_lst, many = True)
        return Response(return_serializer.data)
    

    