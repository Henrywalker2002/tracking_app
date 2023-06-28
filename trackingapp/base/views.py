from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.serializers import ValidationError
import logging
from functools import reduce
import uuid

def validate_ids(exist_ids, object_lst):
    error_lst = []
    for obj in object_lst:
        try:
            id = uuid.UUID(obj.get('id'))
            if id not in exist_ids:
                error_lst.append(f"id {id} is not exist")
        except Exception as e :
            error_lst.append(f"id {obj.get('id')} is not valid")
    if error_lst:
        raise ValidationError(error_lst)

class CustomModelViewSetBase(viewsets.ModelViewSet):
    """
    custom get serializer class to get serializer class base on dict 
    Add action bulk detele, bulk edit
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
        
    @action(methods= ['delete'], detail= False, url_path= 'bulk-delete')
    def bulk_delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        queryset.filter(id__in = serializer.data['ids']).delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    
    @action(methods=['PATCH'], detail=False, url_path='bulk-update')
    def bulk_update(self, request, *args, **kwargs):
        """
        Update field pass by request.body['objects'] + updated_by 
        """
        validate_ids(list(self.get_queryset().values_list('id', flat = True)), request.data.get('objects'))
        instance_lst = []
        fields = {'updated_by'}
        updated_instances = []
        ids = reduce(lambda prev, curr: prev + [curr.get('id')], request.data.get('objects'), [])
        instances = self.get_queryset().filter(id__in = ids)
        serializer = self.get_serializer(instances, request.data['objects'], many = True, partial = True)
        serializer.is_valid(raise_exception = True)
        for obj in request.data['objects']:
            instance = instances.filter(id = obj.pop('id')).get()
            for key,value in obj.items():
                setattr(instance, key, value)
                fields.add(key)
            setattr(instance, 'updated_by', self.request.user)
            instance_lst.append(instance)
        self.get_serializer_class().Meta.model.objects.bulk_update(instance_lst, fields)
        return Response(serializer.data)
    
    @action(methods= ['POST'], detail= False , url_path= 'bulk-create')
    def bulk_create(self, request):
        serializer = self.get_serializer(data = request.data, many = True)
        serializer.is_valid(raise_exception = True)
        instance_lst = []
        for obj in serializer.data:
            instance = self.get_serializer_class().Meta.model(**obj)
            if hasattr(instance, created_by):
                setattr(instance, 'created_by', request.user)
            instance_lst.append(instance)
        self.get_serializer_class().Meta.model.objects.bulk_create(instance_lst)
        return Response(serializer.data)
    