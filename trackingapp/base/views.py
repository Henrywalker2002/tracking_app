from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from functools import reduce
from uuid import UUID
import datetime
from django.utils import timezone


class CustomModelViewSetBase(viewsets.ModelViewSet):
    """
    Inherit from viewsets.ModelViewSet
    Custom get serializer class to get serializer class base on dict only
    """
    serializer_class = {}
    def get_serializer_class(self):
        # ensure that serializer_class must be a dict and have default 
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )
        assert isinstance(self.serializer_class, dict), (
            f"{self.__class__.__name__} serialize_class must be a dict"
        )
        assert "default" in self.serializer_class.keys(), (
            f"{self.__class__.__name__} serializer_class must have default keys"
        )
        
        if self.action in self.serializer_class.keys():
            return self.serializer_class[self.action]
        return self.serializer_class['default']
        
class BulkCreateMixin:
    
    @action(methods= ['POST'], detail= False , url_path= 'bulk-create')
    def bulk_create(self, request):
        serializer = self.get_serializer(data = request.data, many = True)
        serializer.is_valid(raise_exception = True)
        instance_lst = []
        for obj in serializer.data:
            instance = self.get_serializer_class().Meta.model(**obj)
            if hasattr(instance, 'created_by'):
                setattr(instance, 'created_by', request.user)
            instance_lst.append(instance)
        res = self.get_serializer_class().Meta.model.objects.bulk_create(instance_lst)
        res_serializer = self.get_serializer(instance = res, many = True)
        # have not fixed return 
        return Response(res_serializer.data, status=status.HTTP_201_CREATED)

class BulkDeleteMixin:
    
    @action(methods= ['delete'], detail= False, url_path= 'bulk-delete')
    def bulk_delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        queryset.filter(id__in = serializer.data['ids']).delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    
class BulkUpdateMixin:
    """
    Update field pass by request.body['objects'] + updated_by 
    """    
    
    @action(methods=['PUT'], detail=False, url_path='bulk-update')
    def bulk_update(self, request, *args, **kwargs):
        instance_lst = []
        fields = {'updated_by', 'modified_at'}
            
        for obj in request.data:
            
            instance = self.get_queryset().filter(id = obj.get('id'))
            if not instance:
                raise serializers.ValidationError(f"id {obj.get('id')} is not exist")
            instance = instance.get()
            
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
        
class BulkActionBaseModelViewSet(CustomModelViewSetBase, BulkCreateMixin, BulkDeleteMixin):
    """
    Custom get serializer class to get serializer class base on dict 
    Bulk detele, bulk create
    """
    pass 
    

class GetByUserIdMixin: 
    """
    have action get by user id 
    """
    @action(detail= False, url_path="get-by-user-id")
    def get_by_user_id(self, request):
        # if many notification ? 
        param = request.GET 
        if not param.get('id'):
            return Response(data = {"id" : f'must have param query id'}, status= status.HTTP_400_BAD_REQUEST)
        try: 
            id = UUID(param.get('id'))
            instance_lst = self.get_queryset().filter(user_id = id)
            
            page = self.paginate_queryset(instance_lst)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(instance_lst, many=True)
            return Response(serializer.data)

        except ValueError as e:
            return Response(data={"id": f"id {param.get('id')} is not valid"}, status= status.HTTP_400_BAD_REQUEST)

class GetByTimeTrackingIdMixin:
    """
    have action get by time tracking id 
    """
    
    @action(detail= False, url_path= "get-by-time-tracking-id")
    def get_by_time_tracking_id(self, request):
        param = request.GET
        try:
            id = UUID(param.get('id'))
            instance_lst = self.get_queryset().filter(time_tracking_id=id)
            
            page = self.paginate_queryset(instance_lst)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(instance_lst, many=True)
            return Response(serializer.data)
        
        except ValueError as e:
            return Response(data={"id": f"id {param.get('id')} is not valid"}, status=400)