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
    for create and update action, input serializer is key create , update and output is retrieve 
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
    
    def get_serializer(self, *args, **kwargs):

        is_get = kwargs.pop('is_get', False)
        if is_get:
            serializer_class = self.serializer_class.get('retrieve', self.get_serializer_class())
        else :
            serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)
    

    def create(self, request, *args, **kwargs):
        """
        Override to get different input and output serializer
        """
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        
        self.perform_create(serializer)
        instance = serializer.instance
        
        serializer_return = self.get_serializer(instance = instance, is_get = True)
        headers = self.get_success_headers(serializer_return.data)
        return Response(data = serializer_return.data, status= status.HTTP_201_CREATED, headers= headers)
    
    def update(self, request, *args, **kwargs):
        """
        Override to get different input and output serializer
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data, partial =partial)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)
        
        serializer_return = self.get_serializer(instance = instance, is_get = True)
        return Response(data = serializer_return.data)
        
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

        
class BulkActionBaseModelViewSet(CustomModelViewSetBase, BulkCreateMixin, BulkDeleteMixin):
    """
    Custom get serializer class to get serializer class base on dict 
    Bulk detele, bulk create
    """
    pass 
